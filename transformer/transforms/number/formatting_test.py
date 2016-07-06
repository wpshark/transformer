import unittest
import formatting

class TestNumberFormattingTransform(unittest.TestCase):

    def test_formatting(self):
        transformer = formatting.NumberFormattingTransform()

        # Dot for decimal
        self.assertEqual(transformer.transform(u'1,234.5', u'.', 0), u'1,234.5')
        self.assertEqual(transformer.transform(u'1,234.5', u'.', 1), u'1.234,5')
        self.assertEqual(transformer.transform(u'1,234.5', u'.', 2), u'1 234.5')
        self.assertEqual(transformer.transform(u'1,234.5', u'.', 3), u'1 234,5')

        # Comma for decimal
        self.assertEqual(transformer.transform(u'1.234,5', u',', 0), u'1,234.5')
        self.assertEqual(transformer.transform(u'1.234,5', u',', 1), u'1.234,5')
        self.assertEqual(transformer.transform(u'1.234,5', u',', 2), u'1 234.5')
        self.assertEqual(transformer.transform(u'1.234,5', u',', 3), u'1 234,5')

        # Edge cases
        self.assertEqual(transformer.transform(u'123', u'.', 0), u'123') # Short number
        self.assertEqual(transformer.transform(u'123 456 789.0', u'.', 0), u'123,456,789.0') # Long number
        self.assertEqual(transformer.transform(u'1234.567', u'.', 0), u'1,234.567') # Assume groups of three digits
        self.assertEqual(transformer.transform(u'12345', u'.', 0), u'12,345') # Don't assume decimal info
        self.assertEqual(transformer.transform(None, u'.', 0), u'')
        self.assertEqual(transformer.transform(u'0', u'.', 0), u'0')
        self.assertEqual(transformer.transform('-1234', u'.', 0), u'-1,234') # Negative numbers
        self.assertEqual(transformer.transform(u'Something', u'.', 0), u'Something')
