import unittest
import uppercase

class TestStringUppercaseTransform(unittest.TestCase):
    def test_uppercase(self):
        transformer = uppercase.StringUppercaseTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("abcD123"), "ABCD123")
        self.assertEqual(transformer.transform(None), "")
