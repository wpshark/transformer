import unittest
from . import formatting

class TestNumberFormattingTransform(unittest.TestCase):

    def test_formatting(self):
        transformer = formatting.NumberFormattingTransform()

        # Dot for decimal
        self.assertEqual(transformer.transform('1,234.5', '.', 0), '1,234.5')
        self.assertEqual(transformer.transform('1,234.5', '.', 1), '1.234,5')
        self.assertEqual(transformer.transform('1,234.5', '.', 2), '1 234.5')
        self.assertEqual(transformer.transform('1,234.5', '.', 3), '1 234,5')

        # Comma for decimal
        self.assertEqual(transformer.transform('1.234,5', ',', 0), '1,234.5')
        self.assertEqual(transformer.transform('1.234,5', ',', 1), '1.234,5')
        self.assertEqual(transformer.transform('1.234,5', ',', 2), '1 234.5')
        self.assertEqual(transformer.transform('1.234,5', ',', 3), '1 234,5')

        # Edge cases
        self.assertEqual(transformer.transform('123', '.', 0), '123') # Short number
        self.assertEqual(transformer.transform('123 456 789.0', '.', 0), '123,456,789.0') # Long number
        self.assertEqual(transformer.transform('1234.567', '.', 0), '1,234.567') # Assume groups of three digits
        self.assertEqual(transformer.transform('12345', '.', 0), '12,345') # Don't assume decimal info
        self.assertEqual(transformer.transform(None, '.', 0), '')
        self.assertEqual(transformer.transform('', '.', 0), '')
        self.assertEqual(transformer.transform('0', '.', 0), '0')
        self.assertEqual(transformer.transform('-1234', '.', 0), '-1,234') # Negative numbers
        self.assertEqual(transformer.transform('Something', '.', 0), 'Something')
