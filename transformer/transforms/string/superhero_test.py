import unittest
import superhero

class TestStringSuperheroTransform(unittest.TestCase):
    def test_capitalize(self):
        transformer = superhero.StringSuperheroTransform()
        self.assertEqual(transformer.transform(""), "")
        self.assertEqual(transformer.transform("Jordan Sherer"), "Vector Star")
        self.assertEqual(transformer.transform("Clark Kent"), "Frog Squirrel")
        self.assertEqual(transformer.transform(None), "")
