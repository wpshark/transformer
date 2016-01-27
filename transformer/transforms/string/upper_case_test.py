import unittest
import upper_case

class TestStringUppercaseTransform(unittest.TestCase):
    def test_uppercase(self):
        transformer = upper_case.StringUppercaseTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("abcD123"), "ABCD123")
        self.assertEqual(transformer.transform(None), "")
