import unittest
import math_operation

class TestNumberMathTransform(unittest.TestCase):
    def test_math_operation(self):
        transformer = math_operation.NumberMathTransform()
        self.assertEqual(6, transformer.transform_many([1, 2, 3], options={'operation': 'mul'}))
        self.assertEqual(6, transformer.transform_many([1, 2, 3], options={'operation': 'add'}))
        self.assertEqual(-4, transformer.transform_many([1, 2, 3], options={'operation': 'sub'}))
        self.assertEqual([-1, -2, -3], transformer.transform_many([1, 2, 3], options={'operation': 'neg'}))
        self.assertEqual([-1.0, -2.1, -3.2], transformer.transform_many([1.0, 2.1, 3.2], options={'operation': 'neg'}))
        self.assertEqual(0, transformer.transform_many([None], options={'operation': 'add'}))
        self.assertEqual(0, transformer.transform_many([''], options={'operation': 'add'}))
        self.assertEqual(0, transformer.transform_many(['Something'], options={'operation': 'add'}))
        self.assertEqual(0, transformer.transform_many([None, 'Something'], options={'operation': 'add'}))
        self.assertEqual(1, transformer.transform_many(['Something', None, 1], options={'operation': 'add'}))
