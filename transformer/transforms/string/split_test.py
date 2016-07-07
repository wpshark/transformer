import unittest
import split

class TestStringStripTransform(unittest.TestCase):
    def test_split(self):
        transformer = split.StringSplitTransform()

        tests = [
            # input, separator, index, output
            ('a:b', ':', 0, 'a'),
            ('a:b', ':', 1, 'b'),
            ('a:b', ':', -1, 'b'),

            ('a:b', ':', '0', 'a'),
            ('a:b', ':', '1', 'b'),
            ('a:b', ':', '-1', 'b'),

            ('a:b', ':', '0 ', 'a'),
            ('a:b', ':', '1 ', 'b'),
            ('a:b', ':', '-1 ', 'b'),

            ('a:b', ':', 'first', 'a'),
            ('a:b', ':', '...', 'a'),
            ('a:b', ':', 'asdf', 'a'),

            ('a b', '', 0, 'a'),
            ('a b', '', 1, 'b'),
            ('a b', '', -1, 'b'),

            ('hello world', 'wo', 0, 'hello '),
            ('hello world', 'wo', 1, 'rld'),
            ('hello world', 'wo', -1, 'rld'),

            ('a, b, c, d', ', ', 0, 'a'),
            ('a, b, c, d', ', ', 1, 'b'),
            ('a, b, c, d', ', ', -2, 'c'),
            ('a, b, c, d', ', ', -1, 'd'),

            ('a, b, c, d', ', ', 'all', ['a', 'b', 'c', 'd']),
            ('a, b, c, d, ', ', ', 'all', ['a', 'b', 'c', 'd', '']),

            ('hello world', '[:space:]', 0, 'hello'),
            ('hello world', '[:space:]', 1, 'world'),
            ('hello world', '[:space:]', -1, 'world'),

            ('hello  world', '[:s:]', 0, 'hello'),
            ('hello  world', '[:s:]', 1, ''),
            ('hello  world', '[:s:]', -1, 'world'),

            ('b', ',', 0, 'b'),
        ]

        for input_string, separator, index, output_string in tests:
            self.assertEqual(output_string, transformer.transform(input_string, separator=separator, index=index))

    def test_split_empty(self):
        transformer = split.StringSplitTransform()

        self.assertEqual('', transformer.transform('', separator=',', index='all'))
        self.assertEqual('', transformer.transform(None, separator=',', index='all'))

    def test_split_many(self):
        transformer = split.StringSplitTransform()

        self.assertEqual([['a', 'b'], ['c', 'd']], transformer.transform_many(['a,b', 'c,d'], dict(separator=',', index='all')))

    def test_split_many_empty(self):
        transformer = split.StringSplitTransform()

        self.assertEqual(['', ['c', 'd']], transformer.transform_many(['', 'c,d'], dict(separator=',', index='all')))
        self.assertEqual(['', '', ['c', 'd']], transformer.transform_many(['', '', 'c,d'], dict(separator=',', index='all')))
        self.assertEqual(['', ''], transformer.transform_many(['', ''], dict(separator=',', index='all')))

        self.assertEqual(['', ['c', 'd']], transformer.transform_many([None, 'c,d'], dict(separator=',', index='all')))
        self.assertEqual(['', '', ['c', 'd']], transformer.transform_many([None, None, 'c,d'], dict(separator=',', index='all')))
        self.assertEqual(['', ''], transformer.transform_many([None, None], dict(separator=',', index='all')))
