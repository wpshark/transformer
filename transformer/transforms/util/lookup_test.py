import unittest
from . import lookup

class TestUtilLookupTransform(unittest.TestCase):
    def test_lookup_empty(self):
        transformer = lookup.UtilLookupTransform()

        self.assertEqual(transformer.transform('a', table={'a': 1, 'b': 2}, fallback=3), 1)
        self.assertEqual(transformer.transform('asfguy', table={'a': 1, 'b': 2}, fallback=3), 3)
        self.assertEqual(transformer.transform('', table={'a': 1, 'b': 2}, fallback=3), 3)
        self.assertEqual(transformer.transform('', table={'a': 1, 'b': 2, '': 10}, fallback=3), 3)

        self.assertEqual(transformer.transform('a', table={'a': 1, 'b': 2}, fallback=3), 1)
        self.assertEqual(transformer.transform('asfguy', table={'a': 1, 'b': 2}, fallback=3), 3)
        self.assertEqual(transformer.transform('', table={'a': 1, 'b': 2}, fallback=3), 3)
        self.assertEqual(transformer.transform('', table={'a': 1, 'b': 2, '': 10}, fallback='cat'), 'cat')

        self.assertEqual(transformer.transform('nothing'), '')
        self.assertEqual(transformer.transform('something', fallback='something'), 'something')
        self.assertEqual(transformer.transform(None), '')
