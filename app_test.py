import json
import unittest

from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_list_transforms(self):
        response = self.app.get('/')
        transforms = json.loads(response.data)['transforms']
        self.assertIn('string.uppercase', transforms)

    def test_no_transform(self):
        response = self.app.post('/transform', data=json.dumps({}))
        self.assertEqual(400, response.status_code)

    def test_run_transform(self):
        response = self.app.post('/transform', data=json.dumps({'transform': 'string.uppercase', 'inputs': 'abc'}))
        output = json.loads(response.data)['output']
        self.assertEqual('ABC', output)
