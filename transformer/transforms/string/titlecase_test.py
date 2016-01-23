import unittest
import titlecasetransform

class TestStringTitlecaseTransform(unittest.TestCase):
    def test_titlecase(self):
        transformer = titlecasetransform.StringTitlecaseTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("my dog is blue"), "My Dog Is Blue")
        self.assertEqual(transformer.transform(None), "")
