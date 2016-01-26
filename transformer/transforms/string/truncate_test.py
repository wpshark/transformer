import unittest
import truncate

class TestStringTruncateTransform(unittest.TestCase):
    def test_truncate(self):
        transformer = truncate.StringTruncateTransform()
        self.assertEqual(transformer.transform("", 5), "")
        self.assertEqual(transformer.transform("abc", 5), "abc")
        self.assertEqual(transformer.transform("abcde", 5), "abcde")
        self.assertEqual(transformer.transform("abcdef", 5), "abcde")
        self.assertEqual(transformer.transform(None), "")
        self.assertEqual(transformer.transform("abcde", -5), "")

    def test_truncuate_with_ellipsis(self):
        transformer = truncate.StringTruncateTransform()
        self.assertEqual(transformer.transform("abcdefg", 6, append_ellipsis=True), "abc...")
        self.assertEqual(transformer.transform("abcdef", 6, append_ellipsis=True), "abcdef")
        self.assertEqual(transformer.transform("abc", 2, append_ellipsis=True), "ab")
        self.assertEqual(transformer.transform("abcde", 4, append_ellipsis=True), "a...")
