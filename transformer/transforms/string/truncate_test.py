import unittest
import truncate

class TestStringTruncateTransform(unittest.TestCase):
    def test_truncate(self):
        transformer = truncate.StringTruncateTransform()

        self.assertEqual(transformer.transform(None), "")
        self.assertEqual(transformer.transform("", max_length=5), "")
        self.assertEqual(transformer.transform("abc", max_length=5), "abc")
        self.assertEqual(transformer.transform("abcde", max_length=5), "abcde")
        self.assertEqual(transformer.transform("abcdef", max_length=5), "abcde")
        self.assertEqual(transformer.transform("abcde", max_length=-5), "")

    def test_truncate_with_offset(self):
        transformer = truncate.StringTruncateTransform()

        self.assertEqual(transformer.transform("", max_length=5, offset=1), "")
        self.assertEqual(transformer.transform(None, max_length=5, offset=1), "")
        self.assertEqual(transformer.transform("abc", max_length=5, offset=1), "bc")
        self.assertEqual(transformer.transform("abcdef", max_length=3, offset=1), "bcd")
        self.assertEqual(transformer.transform("abcde", max_length=5, offset=-1), "e")
        self.assertEqual(transformer.transform("abcdef", max_length=5, offset=-1), "f")
        self.assertEqual(transformer.transform("abcde", max_length=10, offset=-2), "de")
        self.assertEqual(transformer.transform("abcde", max_length=10, offset=-2, append_ellipsis=True), "...")

    def test_truncate_with_ellipsis(self):
        transformer = truncate.StringTruncateTransform()

        self.assertEqual(transformer.transform("", max_length=2, append_ellipsis=True), "")
        self.assertEqual(transformer.transform(None, max_length=2, append_ellipsis=True), "")
        self.assertEqual(transformer.transform("abcdefg", max_length=6, append_ellipsis=True), "abc...")
        self.assertEqual(transformer.transform("abcdef", max_length=6, append_ellipsis=True), "abc...")
        self.assertEqual(transformer.transform("abc", max_length=2, append_ellipsis=True), "...")
        self.assertEqual(transformer.transform("abcde", max_length=4, append_ellipsis=True), "a...")
