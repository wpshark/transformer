import unittest
import split

class TestStringStripTransform(unittest.TestCase):
    def test_split(self):
        transformer = split.StringSplitTransform()

        tests = [
            # input, separator, index, output
            ('a:b', ':',  0,  'a'),
            ('a:b', ':',  1,  'b'),
            ('a:b', ':', -1, 'b'),

            ('a:b', ':', '0',  'a'),
            ('a:b', ':', '1',  'b'),
            ('a:b', ':', '-1', 'b'),

            ('a:b', ':', '0 ',  'a'),
            ('a:b', ':', '1 ',  'b'),
            ('a:b', ':', '-1 ', 'b'),

            ('a:b', ':', 'first',  'a'),
            ('a:b', ':', '...',  'a'),
            ('a:b', ':', 'asdf', 'a'),

            ('a b', '',  0,  'a'),
            ('a b', '',  1,  'b'),
            ('a b', '', -1, 'b'),

            ('hello world', 'wo',  0, 'hello '),
            ('hello world', 'wo',  1, 'rld'),
            ('hello world', 'wo', -1, 'rld'),

            ('a, b, c, d', ', ',  0, 'a'),
            ('a, b, c, d', ', ',  1, 'b'),
            ('a, b, c, d', ', ', -2, 'c'),
            ('a, b, c, d', ', ', -1, 'd'),
        ]

        for input_string, separator, index, output_string in tests:
            self.assertEqual(output_string, transformer.transform(input_string, separator=separator, index=index))
