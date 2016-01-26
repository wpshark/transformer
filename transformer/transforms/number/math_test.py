import unittest
import math

class TestNumberMathTransform(unittest.TestCase):
    def test_math(self):
        transformer = math.NumberMathTransform()
        self.assertEqual(6, transformer.transform_many([1, 2, 3], options={'operation': 'mul'}))
        self.assertEqual(6, transformer.transform_many([1, 2, 3], options={'operation': 'sum'}))
        self.assertEqual(-4, transformer.transform_many([1, 2, 3], options={'operation': 'sub'}))
        self.assertEqual([-1, -2, -3], transformer.transform_many([1, 2, 3], options={'operation': 'neg'}))
        self.assertEqual([-1.0, -2.1, -3.2], transformer.transform_many([1.0, 2.1, 3.2], options={'operation': 'neg'}))
