import unittest
from app import app
import json


class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_register_user(self):
        data = {'username': 'test_user2', 'password': 'test_password2'}
        response = self.app.post('/register', json=data)
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('user_id', response_data)

    def test_login_user(self):
        data = {'username': 'test_user', 'password': 'test_password'}
        response = self.app.post('/login', json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('user_id', response_data)

    def test_get_all_stocks(self):
        response = self.app.get('/all-stocks')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(isinstance(response_data, list))

    def test_get_user_stocks(self):
        user_id = 1  # Assuming user with ID 1 exists
        response = self.app.get(f'/user-stocks/{user_id}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(isinstance(response_data, list))

    def test_buy_stock(self):
        data = {'user_id': 1, 'stock_id': 1, 'quantity': 2}  # Assuming user and stock exist with these IDs
        response = self.app.post('/buy-stock', json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Stock bought successfully')

    def test_sell_stock(self):
        data = {'user_id': 1, 'stock_id': 1, 'quantity': 5}  # Assuming user and stock exist with these IDs
        response = self.app.post('/sell-stock', json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Stock sold successfully')

    def test_get_user_info(self):
        user_id = 1  # Assuming user with ID 1 exists
        response = self.app.get(f'/user-info/{user_id}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue('user_id' in response_data)
        self.assertTrue('username' in response_data)
        self.assertTrue('balance' in response_data)

if __name__ == '__main__':
    unittest.main()
