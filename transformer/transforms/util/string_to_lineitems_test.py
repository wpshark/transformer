import unittest
import string_to_lineitems

class TestUtilStringToLineItemsTransform(unittest.TestCase):

    def test_string_to_lineitems(self):
        transformer = string_to_lineitems.UtilStringToLineItemsTransform()
        self.assertEqual({u'test lines': [{u'price':'a'},{u'price':'b'},{u'price':'c'},
            {u'price':'d'}]}, transformer.transform(u'test lines', table={u'price':'a,b,c,d'}))
        self.assertEqual({u'Line-item(s)': [{u'price':'a'},{u'price':'b'},{u'price':'c'},
            {u'price':'d'}]}, transformer.transform('', table={u'price':'a,b,c,d'}))
        self.assertEqual({u'Line-item(s)': 
            [{u'price':'a', u'name':'one'},
            {u'price':'b', u'name':'two'},
            {u'price':'c', u'name':'three'},
            {u'price':'d', u'name':'four'}]},
            transformer.transform('', table={u'price':'a,b,c,d', u'name':'one,two,three,four'}))

    def test_string_to_lineitems_variable_length(self):
        transformer = string_to_lineitems.UtilStringToLineItemsTransform()
        self.assertEqual({u'test lines': [{u'price':'a'},{u'price':'b'},{u'price':'c'},
            {u'price':'d'}]}, transformer.transform(u'test lines', table={u'price':'a,b,c,d'}))

    def test_string_to_lineitems_empty(self):
        transformer = string_to_lineitems.UtilStringToLineItemsTransform()
        self.assertEqual({u'Line-item(s)':[]}, transformer.transform('', table={}))
#        self.assertEqual('', transformer.transform(None))
#
