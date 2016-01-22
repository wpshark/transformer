import json
import unittest

from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_list_transforms(self):
        response = self.app.get('/')
        transforms = [v.get('key') for v in json.loads(response.data)['transforms']]
        self.assertIn('string.uppercase', transforms)

    def test_list_transforms_category(self):
        response = self.app.get('/', query_string={'category': 'string'})
        transforms = [v.get('key') for v in json.loads(response.data)['transforms']]
        self.assertIn('string.uppercase', transforms)

    def test_list_transforms_invalid_category(self):
        response = self.app.get('/', query_string={'category': 'astring'})
        transforms = [v.get('key') for v in json.loads(response.data)['transforms']]
        self.assertNotIn('string.uppercase', transforms)

    def test_no_transform(self):
        response = self.app.post('/transform', data=json.dumps({}))
        self.assertEqual(400, response.status_code)

    def test_run_transform(self):
        response = self.app.post('/transform', data=json.dumps({'transform': 'string.uppercase', 'inputs': 'abc'}))
        output = json.loads(response.data)['outputs']
        self.assertEqual('ABC', output)

    def test_run_transform_dotted(self):
        response = self.app.post('/transform', data=json.dumps({
            'transform': 'uppercase',
            'category': 'string',
            'inputs': 'abc'
        }))
        output = json.loads(response.data)['outputs']
        self.assertEqual('ABC', output)

    def test_run_transform_list(self):
        response = self.app.post('/transform', data=json.dumps({'transform': 'string.uppercase', 'inputs': ['abc', 'def']}))
        output = json.loads(response.data)['outputs']
        self.assertEqual(['ABC', 'DEF'], output)

    def test_run_transform_dict(self):
        response = self.app.post('/transform', data=json.dumps({'transform': 'string.uppercase', 'inputs': {'abc': 'def', 'ghi': 'jkl'}}))
        output = json.loads(response.data)['outputs']
        self.assertEqual({'abc': 'DEF', 'ghi': 'JKL'}, output)
