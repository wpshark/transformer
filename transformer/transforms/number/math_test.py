import unittest
import math

class TestNumberMathTransform(unittest.TestCase):
    def test_math(self):
        transformer = math.NumberMathTransform()
        self.assertEqual(6, transformer.transform_many([1, 2, 3], data={'operation': 'mul'}))
        self.assertEqual(6, transformer.transform_many([1, 2, 3], data={'operation': 'sum'}))
        self.assertEqual(-4, transformer.transform_many([1, 2, 3], data={'operation': 'sub'}))
        self.assertEqual([-1, -2, -3], transformer.transform_many([1, 2, 3], data={'operation': 'neg'}))
        self.assertEqual([-1.0, -2.1, -3.2], transformer.transform_many([1.0, 2.1, 3.2], data={'operation': 'neg'}))
