import unittest
import lowercase

class TestStringLowercaseTransform(unittest.TestCase):
    def test_lowercase(self):
        transformer = lowercase.StringLowercaseTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("ABCD123"), "abcd123")
        self.assertEqual(transformer.transform(None), "")
