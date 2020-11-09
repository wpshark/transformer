import unittest
from . import string_to_lineitem

class TestUtilStringToLineItemTransform(unittest.TestCase):

    def test_string_to_lineitem(self):
        transformer = string_to_lineitem.UtilStringToLineItemTransform()
        self.assertEqual(['a', 'b', 'c', 'd'], transformer.transform('a,b,c,d'))
        self.assertEqual(['a', 'b', 'c', 'd', ''], transformer.transform('a,b,c,d,'))

    def test_string_to_lineitem_empty(self):
        transformer = string_to_lineitem.UtilStringToLineItemTransform()
        self.assertEqual('', transformer.transform(''))
        self.assertEqual('', transformer.transform(None))

    def test_string_to_lineitem_many(self):
        transformer = string_to_lineitem.UtilStringToLineItemTransform()
        self.assertEqual([['a', 'b'], ['c', 'd']], transformer.transform_many(['a,b', 'c,d'], options={'separator':','}))

    def test_string_to_lineitem_many_empty(self):
        transformer = string_to_lineitem.UtilStringToLineItemTransform()

        self.assertEqual(['', ['c', 'd']], transformer.transform_many(['', 'c,d'], options={'separator':','}))
        self.assertEqual(['', '', ['c', 'd']], transformer.transform_many(['', '', 'c,d'], options={'separator':','}))
        self.assertEqual(['', ''], transformer.transform_many(['', ''], options={'separator':','}))

        self.assertEqual(['', ['c', 'd']], transformer.transform_many([None, 'c,d'], options={'separator':','}))
        self.assertEqual(['', '', ['c', 'd']], transformer.transform_many([None, None, 'c,d'], options={'separator':','}))
        self.assertEqual(['', ''], transformer.transform_many([None, None], options={'separator':','}))
