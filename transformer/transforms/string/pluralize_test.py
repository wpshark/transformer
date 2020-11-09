import unittest
from . import pluralize

class TestStringPluralizeTransform(unittest.TestCase):
    def test_pluralize(self):
        transformer = pluralize.StringPluralizeTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("frog"), "frogs")
        self.assertEqual(transformer.transform("deer"), "deer")
        self.assertEqual(transformer.transform("child"), "children")
        self.assertEqual(transformer.transform(None), "")
