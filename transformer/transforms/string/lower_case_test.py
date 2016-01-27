import unittest
import lower_case

class TestStringLowercaseTransform(unittest.TestCase):
    def test_lowercase(self):
        transformer = lower_case.StringLowercaseTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("ABCD123"), "abcd123")
        self.assertEqual(transformer.transform(None), "")
