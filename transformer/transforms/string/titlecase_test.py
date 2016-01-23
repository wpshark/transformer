import unittest
import uppercase

class TestStringTitlecaseTransform(unittest.TestCase):
    def test_titlecase(self):
        transformer = uppercase.StringTitlecaseTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("my dog is blue"), "My Dog is Blue")
        self.assertEqual(transformer.transform(None), "")
