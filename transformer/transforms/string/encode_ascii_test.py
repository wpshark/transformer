import unittest
import encode_ascii

class TestStringEncodeasciiTransform(unittest.TestCase):
    def test_encodeascii(self):
        transformer = encode_ascii.StringEncodeasciiTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform(u'\u200cN\u200co\u200cv\u200c'), "Nov")
        self.assertEqual(transformer.transform(None), "")
