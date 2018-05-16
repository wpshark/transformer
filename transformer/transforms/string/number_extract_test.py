import unittest
import number_extract

class TestStringNumberExtractTransform(unittest.TestCase):
    def test_number_extract(self):
        transformer = number_extract.StringNumberExtractTransform()
        self.assertEqual(transformer.transform(u''), u'')
        self.assertEqual(transformer.transform(None), u'')
        self.assertEqual(transformer.transform(u'I have no dogs'), u'')
        self.assertEqual(transformer.transform(u'I have 3 dogs'), u'3')
        self.assertEqual(transformer.transform(u'I have 3,124 dogs'), u'3,124')
        self.assertEqual(transformer.transform(u'I have 3 124 dogs'), u'3')
        self.assertEqual(transformer.transform(u'I have 3.124 dogs'), u'3.124')
        self.assertEqual(transformer.transform(u'I need 5 things. and something else. .'), u'5')
        self.assertEqual(transformer.transform(u'I need five+5, you?'), u'+5')
        self.assertEqual(transformer.transform(u'It\'s -3 below outside!'), u'-3')

        # No punctuation false positives
        self.assertEqual(transformer.transform(u'.', u''))
        self.assertEqual(transformer.transform(u',', u''))
        self.assertEqual(transformer.transform(u',,', u''))
        self.assertEqual(transformer.transform(u',.', u''))
        self.assertEqual(transformer.transform(u'+', u''))
        self.assertEqual(transformer.transform(u'-', u''))
        self.assertEqual(transformer.transform(u'+,', u''))
        self.assertEqual(transformer.transform(u'+,.', u''))

        # Trailing and leading punctuation should not be captured except +/-
        self.assertEqual(transformer.transform(u'3.', u'3'))
        self.assertEqual(transformer.transform(u'3,', u'3'))
        self.assertEqual(transformer.transform(u',3', u'3'))
        self.assertEqual(transformer.transform(u'3,000.', u'3,000'))
        self.assertEqual(transformer.transform(u'3,000,', u'3,000,'))
        self.assertEqual(transformer.transform(u'+3,000', u'+3,000'))
        self.assertEqual(transformer.transform(u'-3,000', u'-3,000'))
