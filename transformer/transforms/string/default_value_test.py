import unittest
from . import default_value

class TestStringDefaultValueTransform(unittest.TestCase):
    def test_default_value(self):
        transformer = default_value.StringDefaultValueTransform()

        self.assertEqual(transformer.transform("", default_value="test"), "test")
        self.assertEqual(transformer.transform("", default_value="test"), "test")
        self.assertEqual(transformer.transform(None, default_value="test"), "test")

        self.assertEqual(transformer.transform("a", default_value="test"), "a")
        self.assertEqual(transformer.transform(0, default_value="test"), 0)
        self.assertEqual(transformer.transform(1, default_value="test"), 1)
        self.assertEqual(transformer.transform(True, default_value="test"), True)
        self.assertEqual(transformer.transform(False, default_value="test"), False)
