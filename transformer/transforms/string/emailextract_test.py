import unittest
import emailextract

class TestStringEmailExtractTransform(unittest.TestCase):
    def test_emailextract(self):
        transformer = emailextract.StringEmailExtractTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("my email is thomas@hils.us"), "thomas@hils.us")
        self.assertEqual(transformer.transform(None), "")
        self.assertEqual(transformer.transform("my email is broken thomas@hils .com"), "")
