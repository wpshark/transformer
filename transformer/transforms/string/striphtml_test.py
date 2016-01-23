import unittest
import striphtml

class TestStringStripHtmlTransform(unittest.TestCase):
    def test_striphtml(self):
        transformer = striphtml.StringStripHtmlTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("<b>Bold</b>"), "Bold")
        self.assertEqual(transformer.transform(None), "")
