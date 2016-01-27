import unittest
import title_case

class TestStringTitlecaseTransform(unittest.TestCase):
    def test_titlecase(self):
        transformer = title_case.StringTitlecaseTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("my dog is blue"), "My Dog Is Blue")
        self.assertEqual(transformer.transform(None), "")
