import unittest
import json
from data.api import app

class TestAnalyzeBitvavo(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_analyze_bitvavo(self):
        response = self.app.get('/api/analyze_bitvavo')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)  # Check if the response is a list

if __name__ == '__main__':
    unittest.main()
