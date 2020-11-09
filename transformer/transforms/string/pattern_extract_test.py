import unittest
from . import pattern_extract

class TestStringPatternExtractTransform(unittest.TestCase):
    def test_pattern_extract(self):
        transformer = pattern_extract.StringPatternExtractTransform()
        pattern = "f([o]+)( b(?P<named>[a]+)r)?"
        self.assertEqual(transformer.transform("", pattern), {'_matched': False})
        self.assertEqual(transformer.transform(None, pattern), {'_matched': False})
        self.assertEqual(transformer.transform(
            "Hello foo folks and another foo bar I will not catch", pattern),
            {0: 'oo', 1: None, 2: None, 'named': None, '_end': 9, '_start': 6, '_matched': True}
        )
        self.assertEqual(transformer.transform(
            "Hello foo bar folks and another foo I will not catch", pattern),
            {0: 'oo', 1: ' bar', 2: 'a', '_end': 13, '_start': 6, '_matched': True, 'named': 'a'}
        )

    def test_pattern_extract_without_match_groups(self):
        transformer = pattern_extract.StringPatternExtractTransform()
        pattern = "foo"
        self.assertEqual(transformer.transform("", pattern), {'_matched': False})
        self.assertEqual(transformer.transform(None, pattern), {'_matched': False})
        self.assertEqual(transformer.transform(
            "Hello foo bar folks and another foo I will not catch", pattern),
            {0: 'foo', '_matched': True, "_start": 6, "_end": 9}
        )

