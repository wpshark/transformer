import unittest
import capitalize

class TestStringCapitalizeTransform(unittest.TestCase):
    def test_capitalize(self):
        transformer = capitalize.StringCapitalizeTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("on the origin OF 34 species"), "On The Origin Of 34 Species")
        self.assertEqual(transformer.transform(None), "")
