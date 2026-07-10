import unittest

from app import create_app
from app.extensions import db
from app.models import Customer
from app.auth import encode_token
from werkzeug.security import generate_password_hash


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')

        # A pre-existing customer, used for GET/PUT/DELETE/login tests.
        self.customer = Customer(
            name="Test User",
            email="test@email.com",
            phone="555-000-0000",
            password=generate_password_hash("password123")
        )

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
            self.customer_id = self.customer.id

        # Build a token directly (same approach as the login test helper),
        # so PUT/DELETE tests don't depend on hitting the login endpoint.
        with self.app.app_context():
            self.token = encode_token(self.customer_id)

        self.client = self.app.test_client()
        self.auth_headers = {'Authorization': f"Bearer {self.token}"}

    # ---------------- Create ----------------

    def test_create_customer(self):
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "555-123-4567",
            "password": "supersecret123"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Jane Doe")
        self.assertEqual(response.json['email'], "jane@example.com")
        # Password should never come back in the response.
        self.assertNotIn('password', response.json)

    def test_create_customer_missing_fields(self):
        # email is required by the model (nullable=False); leaving it out
        # should trigger a validation error before anything hits the DB.
        payload = {"name": "No Email", "password": "somepassword"}
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json)

    # ---------------- Get all (paginated) ----------------

    def test_get_customers(self):
        response = self.client.get('/customers/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertIn('customers', response.json)
        self.assertEqual(response.json['total'], 1)

    # ---------------- Get one ----------------

    def test_get_customer(self):
        response = self.client.get(f'/customers/{self.customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], "test@email.com")

    def test_get_customer_not_found(self):
        response = self.client.get('/customers/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    # ---------------- Login ----------------

    def test_login_valid(self):
        credentials = {"email": "test@email.com", "password": "password123"}
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_login_invalid(self):
        credentials = {"email": "test@email.com", "password": "wrong-password"}
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json)

    # ---------------- Update ----------------

    def test_update_customer(self):
        payload = {"name": "Updated Name"}
        response = self.client.put(
            f'/customers/{self.customer_id}', json=payload, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Name")
        self.assertEqual(response.json['email'], "test@email.com")

    def test_update_customer_no_token(self):
        payload = {"name": "Sneaky Update"}
        response = self.client.put(f'/customers/{self.customer_id}', json=payload)
        self.assertEqual(response.status_code, 401)

    def test_update_customer_wrong_customer(self):
        # Create a second customer, then try to update THEM using our token.
        with self.app.app_context():
            other = Customer(
                name="Other Person", email="other@email.com",
                password=generate_password_hash("pw")
            )
            db.session.add(other)
            db.session.commit()
            other_id = other.id

        payload = {"name": "Hijacked"}
        response = self.client.put(
            f'/customers/{other_id}', json=payload, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 403)

    # ---------------- Delete ----------------

    def test_delete_customer_no_token(self):
        response = self.client.delete(f'/customers/{self.customer_id}')
        self.assertEqual(response.status_code, 401)

    def test_delete_customer(self):
        response = self.client.delete(
            f'/customers/{self.customer_id}', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

        # Confirm it's really gone.
        follow_up = self.client.get(f'/customers/{self.customer_id}')
        self.assertEqual(follow_up.status_code, 404)


if __name__ == '__main__':
    unittest.main()