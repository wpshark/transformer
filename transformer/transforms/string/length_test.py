import unittest
import length


class TestStringLengthTransform(unittest.TestCase):
    def test_length(self):
        transformer = length.StringLengthTransform()

        self.assertEqual(transformer.transform(None), 0)
        self.assertEqual(transformer.transform(""), 0)
        self.assertEqual(transformer.transform(u""), 0)
        self.assertEqual(transformer.transform("a"), 1)
        self.assertEqual(transformer.transform(u"a"), 1)
        self.assertEqual(transformer.transform("abcde"), 5)
        self.assertEqual(transformer.transform("abc\r\nde"), 7)
        self.assertEqual(transformer.transform("\n"), 1)

    def test_ignore_whitespace(self):
        transformer = length.StringLengthTransform()

        self.assertEqual(transformer.transform(None, ignore_whitespace=True), 0)
        self.assertEqual(transformer.transform(" ", ignore_whitespace=True), 0)
        self.assertEqual(transformer.transform(u" ", ignore_whitespace=True), 0)
        self.assertEqual(transformer.transform("\t \n", ignore_whitespace=True), 0)
        self.assertEqual(transformer.transform(u"\t \n", ignore_whitespace=True), 0)
        self.assertEqual(transformer.transform("ab cd\te", ignore_whitespace=True), 5)
        self.assertEqual(transformer.transform("abc\r\nde", ignore_whitespace=True), 5)
        self.assertEqual(transformer.transform("\n", ignore_whitespace=True), 0)
