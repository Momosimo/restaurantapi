import unittest
from app import app, load_restaurants
from datetime import datetime
import json

class TestRestaurantAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.restaurants = load_restaurants()

    def test_valid_datetime(self):
        """Test for valid datetime."""
        response = self.app.get('/restaurants/open?datetime=2025-03-23T12:00:00')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('datetime', data)
        self.assertIn('open_restaurants', data)

    def test_missing_datetime(self):
        """Test for missing datetime parameter."""
        response = self.app.get('/restaurants/open')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_invalid_datetime(self):
        """Test for invalid datetime format."""
        response = self.app.get('/restaurants/open?datetime=tomorrow')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
