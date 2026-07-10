import unittest

from app import create_app
from app.extensions import db
from app.models import Inventory


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestingConfig')

        self.part = Inventory(name="Brake Pad Set", price=45.99)

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.part)
            db.session.commit()
            self.part_id = self.part.id

        self.client = self.app.test_client()

    # ---------------- Create ----------------

    def test_create_part(self):
        payload = {"name": "Oil Filter", "price": 12.5}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Oil Filter")

    def test_create_part_missing_fields(self):
        payload = {"name": "No Price"}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('price', response.json)

    # ---------------- Get all ----------------

    def test_get_parts(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    # ---------------- Get one ----------------

    def test_get_part(self):
        response = self.client.get(f'/inventory/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Brake Pad Set")

    def test_get_part_not_found(self):
        response = self.client.get('/inventory/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    # ---------------- Update ----------------

    def test_update_part(self):
        payload = {"price": 39.99}
        response = self.client.put(f'/inventory/{self.part_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['price'], 39.99)
        self.assertEqual(response.json['name'], "Brake Pad Set")

    def test_update_part_not_found(self):
        response = self.client.put('/inventory/9999', json={"price": 1.0})
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    # ---------------- Delete ----------------

    def test_delete_part(self):
        response = self.client.delete(f'/inventory/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

        follow_up = self.client.get(f'/inventory/{self.part_id}')
        self.assertEqual(follow_up.status_code, 404)

    def test_delete_part_not_found(self):
        response = self.client.delete('/inventory/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)


if __name__ == '__main__':
    unittest.main()