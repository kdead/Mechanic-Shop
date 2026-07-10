import unittest

from app import create_app
from app.extensions import db
from app.models import Mechanic, ServiceTicket, Customer
from werkzeug.security import generate_password_hash


class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')

        self.mechanic = Mechanic(
            name="Sam Torres", email="sam@example.com",
            phone="555-987-6543", salary=55000.0
        )

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
            self.mechanic_id = self.mechanic.id

        self.client = self.app.test_client()

    # ---------------- Create ----------------

    def test_create_mechanic(self):
        payload = {
            "name": "Alex Rivera",
            "email": "alex@example.com",
            "phone": "555-111-2222",
            "salary": 60000.0
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Alex Rivera")

    def test_create_mechanic_missing_fields(self):
        payload = {"phone": "555-111-2222"}
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json)
        self.assertIn('email', response.json)

    # ---------------- Get all ----------------

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], "Sam Torres")

    # ---------------- Update ----------------

    def test_update_mechanic(self):
        payload = {"salary": 65000.0}
        response = self.client.put(f'/mechanics/{self.mechanic_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['salary'], 65000.0)
        self.assertEqual(response.json['name'], "Sam Torres")

    def test_update_mechanic_not_found(self):
        response = self.client.put('/mechanics/9999', json={"salary": 1.0})
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    # ---------------- Delete ----------------

    def test_delete_mechanic(self):
        response = self.client.delete(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_delete_mechanic_not_found(self):
        response = self.client.delete('/mechanics/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    # ---------------- Most tickets ----------------

    def test_mechanics_by_ticket_count(self):
        # Give our mechanic a ticket so the ranking has something to sort.
        with self.app.app_context():
            customer = Customer(
                name="Ticket Owner", email="owner@example.com",
                password=generate_password_hash("pw")
            )
            db.session.add(customer)
            db.session.commit()

            ticket = ServiceTicket(
                VIN="1HGCM82633A004352", service_desc="Oil change",
                customer_id=customer.id
            )
            mechanic = db.session.get(Mechanic, self.mechanic_id)
            ticket.mechanics.append(mechanic)
            db.session.add(ticket)
            db.session.commit()

        response = self.client.get('/mechanics/most-tickets')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], "Sam Torres")


if __name__ == '__main__':
    unittest.main()