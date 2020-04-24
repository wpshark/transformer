import json
import unittest

from transformer.app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_list_transforms(self):
        response = self.app.get('/')
        transforms = [v.get('key') for v in json.loads(response.data)['transforms']]
        self.assertIn('string.upper_case', transforms)

    def test_list_transforms_category(self):
        response = self.app.get('/', query_string={'category': 'string'})
        transforms = [v.get('key') for v in json.loads(response.data)['transforms']]
        self.assertIn('string.upper_case', transforms)

    def test_list_transforms_invalid_category(self):
        response = self.app.get('/', query_string={'category': 'astring'})
        transforms = [v.get('key') for v in json.loads(response.data)['transforms']]
        self.assertEqual([], transforms)

    def test_no_transform(self):
        response = self.app.post('/transform', data=json.dumps({'inputs': ['1']}))
        self.assertEqual(400, response.status_code)
        output = json.loads(response.data)
        self.assertIn('Missing transform', output['message'])

    def test_no_input(self):
        response = self.app.post('/transform', data=json.dumps({'transform': 'string.upper_case'}))
        self.assertEqual(200, response.status_code)
        output = json.loads(response.data)['outputs']
        self.assertEqual('', output)

    def test_invalid_transform(self):
        response = self.app.post('/transform', data=json.dumps({'transform': 'does-not-exist', 'inputs': []}))
        self.assertEqual(404, response.status_code)

    def test_run_transform(self):
        response = self.app.post('/transform', data=json.dumps({'transform': 'string.upper_case', 'inputs': 'abc'}))
        output = json.loads(response.data)['outputs']
        self.assertEqual('ABC', output)

    def test_run_transform_dotted(self):
        response = self.app.post('/transform', data=json.dumps({
            'transform': 'upper_case',
            'category': 'string',
            'inputs': 'abc'
        }))
        output = json.loads(response.data)['outputs']
        self.assertEqual('ABC', output)

    def test_run_transform_list(self):
        response = self.app.post('/transform', data=json.dumps({'transform': 'string.upper_case', 'inputs': ['abc', 'def']}))
        output = json.loads(response.data)['outputs']
        self.assertEqual(['ABC', 'DEF'], output)

    def test_run_transform_dict(self):
        response = self.app.post('/transform', data=json.dumps({'transform': 'string.upper_case', 'inputs': {'abc': 'def', 'ghi': 'jkl'}}))
        output = json.loads(response.data)['outputs']
        self.assertEqual({'abc': 'DEF', 'ghi': 'JKL'}, output)

    def test_run_transform_split(self):
        response = self.app.post('/transform', data=json.dumps({
            'transform': 'string.split',
            'inputs': 'a,b,c',
            'separator': ',',
            'index': 'all'
        }))
        output = json.loads(response.data)['outputs']
        self.assertEqual(['a','b','c'], output)