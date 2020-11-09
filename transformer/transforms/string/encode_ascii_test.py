import unittest
from . import encode_ascii

class TestStringEncodeasciiTransform(unittest.TestCase):
    def test_encodeascii(self):
        transformer = encode_ascii.StringEncodeasciiTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform('ko\u017eu\u0161\u010dek'), "kozuscek")
        self.assertEqual(transformer.transform(None), "")
