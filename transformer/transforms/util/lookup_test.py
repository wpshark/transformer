import unittest
import lookup

class TestUtilLookupTransform(unittest.TestCase):
    def test_lookup_empty(self):
        transformer = lookup.UtilLookupTransform()

        self.assertEquals(transformer.transform({'a': 1, 'b': 2}, key='a', fallback=3), 1)
        self.assertEquals(transformer.transform({'a': 1, 'b': 2}, key='asfguy', fallback=3), 3)
        self.assertEquals(transformer.transform({'a': 1, 'b': 2}, key='', fallback=3), 3)
        self.assertEquals(transformer.transform({'a': 1, 'b': 2, '': 10}, key='', fallback=3), 3)
