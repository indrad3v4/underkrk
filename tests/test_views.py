import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from quart import Quart, request, jsonify
from app.views import app

class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Welcome to UnderKrakow Rave!', result.data)

    def test_webhook(self):
        result = self.app.post('/webhook', json={})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b'OK')

if __name__ == '__main__':
    unittest.main()
