import unittest
import lineitem_to_string_v2


class TestUtilLineItemToStringV2Transform(unittest.TestCase):

    def test_lineitem_to_string_v2_empty(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()

        self.assertEqual('', transformer.transform_many([], options={'separator':','}))
        self.assertEqual('', transformer.transform_many([''], options={'separator':','}))

    def test_lineitem_to_string_v2_many_empty(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()

        self.assertEqual(',c,d', transformer.transform_many(['', 'c', 'd'], options={'separator':','}))
        self.assertEqual(',,c,d', transformer.transform_many(['', '', 'c,d'], options={'separator':','}))
        self.assertEqual(',', transformer.transform_many(['', ''], options={'separator':','}))
        self.assertEqual('c,d,', transformer.transform_many(['c', 'd', ''], options={'separator':','}))
        self.assertEqual(',,c,d', transformer.transform_many(['', '', 'c,d'], options={'separator':','}))
        self.assertEqual(',', transformer.transform_many(['', ''], options={'separator':','}))

    def test_lineitem_to_string_v2_one(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual('a', transformer.transform_many(['a'], options={'separator':','}))

    def test_lineitem_to_string_v2_many(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual('a,b,c,d', transformer.transform_many(['a,b', 'c,d'], options={'separator':','}))
        self.assertEqual('a,b,c,d', transformer.transform_many(['a', 'b', 'c', 'd'], options={'separator':','}))
        self.assertEqual('a,b,c,d', transformer.transform_many(['a,b,c,d'], options={'separator':','}))

    def test_lineitem_to_string_v2_other_separator(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual('a b c d', transformer.transform_many(['a', 'b', 'c', 'd'], options={'separator':'[:space:]'}))
        self.assertEqual('a b c d', transformer.transform_many(['a', 'b', 'c', 'd'], options={'separator':'[:s:]'}))
        self.assertEqual('a;b;c;d', transformer.transform_many(['a', 'b', 'c', 'd'], options={'separator':';'}))

    def test_lineitem_to_string_v2_nolineitem(self):
        transformer = lineitem_to_string_v2.UtilLineItemToStringV2Transform()
        self.assertEqual('abcd', transformer.transform_many('abcd', options={'separator':'[:space:]'}))
