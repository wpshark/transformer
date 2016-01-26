import unittest
import trim_space

class TestStringTrimSpaceTransform(unittest.TestCase):
    def test_truncate(self):
        transformer = trim_space.StringTrimSpaceTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("   abcD123   "), "abcD123")
        self.assertEqual(transformer.transform("   This is a test   "), "This is a test")
        self.assertEqual(transformer.transform(None), "")
