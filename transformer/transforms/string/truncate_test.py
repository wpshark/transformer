import unittest
import truncate

class TestStringTruncateTransform(unittest.TestCase):
    def test_truncate(self):
        transformer = truncate.StringTruncateTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("   abcD123   "), "abcD123")
        self.assertEqual(transformer.transform("   This is a test   "), "This is a test")
        self.assertEqual(transformer.transform(None), "")
