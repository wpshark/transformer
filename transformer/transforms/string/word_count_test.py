import unittest
from . import word_count

class TestWordCount(unittest.TestCase):
    def test_wordcount(self):
        transformer = word_count.StringWordCountTransform()
        self.assertEqual(transformer.transform(''), 0)
        self.assertEqual(transformer.transform('This is a test'), 4)
        self.assertEqual(transformer.transform('New Line Test\nsecond line \nthird line'), 7)
        self.assertEqual(transformer.transform(None), 0)
        self.assertEqual(transformer.transform(' '), 0)
        self.assertEqual(transformer.transform('\n'), 0)
        self.assertEqual(transformer.transform('0 0 0 0'), 4)
