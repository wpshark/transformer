import unittest
from . import number_extract

class TestStringNumberExtractTransform(unittest.TestCase):
    def test_number_extract(self):
        transformer = number_extract.StringNumberExtractTransform()
        self.assertEqual(transformer.transform(''), '')
        self.assertEqual(transformer.transform(None), '')
        self.assertEqual(transformer.transform('I have no dogs'), '')
        self.assertEqual(transformer.transform('I have 3 dogs'), '3')
        self.assertEqual(transformer.transform('I have 3,124 dogs'), '3,124')
        self.assertEqual(transformer.transform('I have 3 124 dogs'), '3')
        self.assertEqual(transformer.transform('I have 3.124 dogs'), '3.124')
        self.assertEqual(transformer.transform('I need 5 things. and something else. .'), '5')
        self.assertEqual(transformer.transform('I need five+5, you?'), '+5')
        self.assertEqual(transformer.transform('It\'s -3 below outside!'), '-3')

        # No punctuation false positives
        self.assertEqual(transformer.transform('.'), '')
        self.assertEqual(transformer.transform(','), '')
        self.assertEqual(transformer.transform(',,'), '')
        self.assertEqual(transformer.transform(',.'), '')
        self.assertEqual(transformer.transform('+'), '')
        self.assertEqual(transformer.transform('-'), '')
        self.assertEqual(transformer.transform('+,'), '')
        self.assertEqual(transformer.transform('+,.'), '')

        # Trailing and leading punctuation should not be captured except +/-
        self.assertEqual(transformer.transform('3.'), '3')
        self.assertEqual(transformer.transform('3,'), '3')
        self.assertEqual(transformer.transform(',3'), '3')
        self.assertEqual(transformer.transform('3,000.'), '3,000')
        self.assertEqual(transformer.transform('3,000,'), '3,000')
        self.assertEqual(transformer.transform('+3,000'), '+3,000')
        self.assertEqual(transformer.transform('-3,000'), '-3,000')
