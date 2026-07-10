import unittest

from app import create_app
from app.extensions import db
from app.models import Customer, Mechanic, ServiceTicket, Inventory
from app.auth import encode_token
from werkzeug.security import generate_password_hash


class TestServiceTicket(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')

        self.customer = Customer(
            name="Ticket Owner", email="owner@example.com",
            password=generate_password_hash("pw")
        )
        self.mechanic = Mechanic(name="Sam Torres", email="sam@example.com", salary=55000.0)
        self.part = Inventory(name="Brake Pad Set", price=45.99)

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add_all([self.customer, self.mechanic, self.part])
            db.session.commit()
            self.customer_id = self.customer.id
            self.mechanic_id = self.mechanic.id
            self.part_id = self.part.id

            ticket = ServiceTicket(
                VIN="1HGCM82633A004352", service_date="2026-07-06",
                service_desc="Brake pad replacement", customer_id=self.customer_id
            )
            db.session.add(ticket)
            db.session.commit()
            self.ticket_id = ticket.id

            self.token = encode_token(self.customer_id)

        self.client = self.app.test_client()
        self.auth_headers = {'Authorization': f"Bearer {self.token}"}

    # ---------------- Create ----------------

    def test_create_service_ticket(self):
        payload = {
            "VIN": "2T1BR32E34C123456",
            "service_date": "2026-08-01",
            "service_desc": "Tire rotation",
            "customer_id": self.customer_id
        }
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['service_desc'], "Tire rotation")

    def test_create_service_ticket_missing_fields(self):
        payload = {"service_desc": "No VIN or customer"}
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('VIN', response.json)
        self.assertIn('customer_id', response.json)

    # ---------------- Get all ----------------

    def test_get_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    # ---------------- Assign mechanic ----------------

    def test_assign_mechanic(self):
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_assign_mechanic_already_assigned(self):
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}'
        )
        self.assertEqual(response.status_code, 400)

    def test_assign_mechanic_not_found(self):
        response = self.client.put(f'/service-tickets/9999/assign-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 404)

    # ---------------- Remove mechanic ----------------

    def test_remove_mechanic(self):
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}'
        )
        self.assertEqual(response.status_code, 200)

    def test_remove_mechanic_not_assigned(self):
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}'
        )
        self.assertEqual(response.status_code, 400)

    # ---------------- Bulk edit mechanics ----------------

    def test_edit_ticket_mechanics(self):
        payload = {"add_ids": [self.mechanic_id], "remove_ids": []}
        response = self.client.put(f'/service-tickets/{self.ticket_id}/edit', json=payload)
        self.assertEqual(response.status_code, 200)

    def test_edit_ticket_mechanics_not_found(self):
        payload = {"add_ids": [self.mechanic_id], "remove_ids": []}
        response = self.client.put('/service-tickets/9999/edit', json=payload)
        self.assertEqual(response.status_code, 404)

    # ---------------- My tickets ----------------

    def test_get_my_tickets(self):
        response = self.client.get('/service-tickets/my-tickets', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_my_tickets_no_token(self):
        response = self.client.get('/service-tickets/my-tickets')
        self.assertEqual(response.status_code, 401)

    # ---------------- Add part ----------------

    def test_add_part_to_ticket(self):
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_add_part_to_ticket_already_added(self):
        self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}')
        response = self.client.put(
            f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}'
        )
        self.assertEqual(response.status_code, 400)

    def test_add_part_to_ticket_not_found(self):
        response = self.client.put(f'/service-tickets/9999/add-part/{self.part_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()