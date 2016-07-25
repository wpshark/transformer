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
