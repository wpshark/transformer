import unittest
import lookup

class TestUtilLookupTransform(unittest.TestCase):
    def test_lookup_empty(self):
        transformer = lookup.UtilLookupTransform()

        self.assertEquals(transformer.transform('a', table={'a': 1, 'b': 2}, fallback=3), 1)
        self.assertEquals(transformer.transform('asfguy', table={'a': 1, 'b': 2}, fallback=3), 3)
        self.assertEquals(transformer.transform('', table={'a': 1, 'b': 2}, fallback=3), 3)
        self.assertEquals(transformer.transform('', table={'a': 1, 'b': 2, '': 10}, fallback=3), 3)

        self.assertEquals(transformer.transform(u'a', table={'a': 1, u'b': 2}, fallback=3), 1)
        self.assertEquals(transformer.transform(u'asfguy', table={'a': 1, u'b': 2}, fallback=3), 3)
        self.assertEquals(transformer.transform(u'', table={'a': 1, u'b': 2}, fallback=3), 3)
        self.assertEquals(transformer.transform(u'', table={'a': 1, u'b': 2, '': 10}, fallback=u'cat'), u'cat')

        self.assertEquals(transformer.transform(u'nothing'), u'')
