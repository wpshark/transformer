import unittest
import pattern_extract

class TestStringPatternExtractTransform(unittest.TestCase):
    def test_pattern_extract(self):
        transformer = pattern_extract.StringPatternExtractTransform()
        pattern = "f([o]+)( b(?P<named>[a]+)r)?"
        self.assertEqual(transformer.transform("", pattern), "")
        self.assertEqual(transformer.transform(None, pattern), "")
        self.assertEqual(transformer.transform(
            "Hello foo folks and another foo bar I will not catch", pattern),
            {0: 'oo', 1: None, 2: None, 'named': None, '_end': 9, '_start': 6, '_matched': True}
        )
        self.assertEqual(transformer.transform(
            "Hello foo bar folks and another foo I will not catch", pattern),
            {0: 'oo', 1: ' bar', 2: 'a', '_end': 13, '_start': 6, '_matched': True, 'named': 'a'}
        )