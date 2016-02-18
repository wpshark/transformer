import transformer.util as util

import unittest

class TestApp(unittest.TestCase):
    def test_util_tdelta(self):
        self.assertEqual(5, util.tdelta('5 years').get('years'))
        self.assertEqual(5, util.tdelta('5 years 3 months').get('years'))
        self.assertEqual(3, util.tdelta('5 years 3 months').get('months'))
        self.assertEqual(1, util.tdelta('5 years 3 months 1 second').get('seconds'))
        self.assertEqual(4, util.tdelta('5 years 3 months 1 second 4 minutes').get('minutes'))
        self.assertEqual(-5, util.tdelta('5 years -3 months 1 seconds 4 minutes -2 months').get('months'))
        self.assertEqual(1, util.tdelta('5 year -3 month 1 second 4 minute -2 month').get('seconds'))
        self.assertEqual(1, util.tdelta('-+ 1 day - 1 week').get('days'))
        self.assertEqual(-1, util.tdelta('-+ 1 day - 1 week').get('weeks'))
        self.assertEqual(1, util.tdelta('+1 day').get('days'))

    def test_util_tdelta_legacy(self):
        self.assertEqual(1, util.tdelta('+1d').get('days'))
        self.assertEqual(-1, util.tdelta('+1d -1h').get('hours'))
        self.assertEqual(-1, util.tdelta('+1d -1h').get('hours'))
        self.assertEqual(5, util.tdelta('+1d -1h +5m').get('minutes'))

        delta = util.tdelta('1dd')
        self.assertEqual(0, delta.get('days'))
        self.assertEqual(0, delta.get('hours'))
        self.assertEqual(0, delta.get('minutes'))

        delta = util.tdelta('1dd 5m')
        self.assertEqual(0, delta.get('days'))
        self.assertEqual(0, delta.get('hours'))
        self.assertEqual(5, delta.get('minutes'))

    def test_util_tdelta_combined(self):
        delta = util.tdelta('-5 days +1d 10 hours -1h +16 minutes +5m')
        self.assertEqual(-4, delta.get('days'))
        self.assertEqual(9, delta.get('hours'))
        self.assertEqual(21, delta.get('minutes'))

        delta = util.tdelta('+1d -5 days -1h 10 hours +5m +16 minutes')
        self.assertEqual(-4, delta.get('days'))
        self.assertEqual(9, delta.get('hours'))
        self.assertEqual(21, delta.get('minutes'))

    def test_util_tdelta_all(self):
        tests = [
            ('years',   [0, 1, 2, -1, -10, 10], 'y'),
            ('years',   [0, 1, 2, -1, -10, 10], 'yr'),
            ('years',   [0, 1, 2, -1, -10, 10], 'yrs'),
            ('years',   [0, 1, 2, -1, -10, 10], 'year'),
            ('years',   [0, 1, 2, -1, -10, 10], 'years'),
            ('months',  [0, 1, 2, -1, -10, 10], 'mo'),
            ('months',  [0, 1, 2, -1, -10, 10], 'month'),
            ('months',  [0, 1, 2, -1, -10, 10], 'months'),
            ('weeks',   [0, 1, 2, -1, -10, 10], 'w'),
            ('weeks',   [0, 1, 2, -1, -10, 10], 'wk'),
            ('weeks',   [0, 1, 2, -1, -10, 10], 'wks'),
            ('weeks',   [0, 1, 2, -1, -10, 10], 'week'),
            ('weeks',   [0, 1, 2, -1, -10, 10], 'weeks'),
            ('days',    [0, 1, 2, -1, -10, 10], 'd'),
            ('days',    [0, 1, 2, -1, -10, 10], 'day'),
            ('days',    [0, 1, 2, -1, -10, 10], 'days'),
            ('hours',   [0, 1, 2, -1, -10, 10], 'h'),
            ('hours',   [0, 1, 2, -1, -10, 10], 'hr'),
            ('hours',   [0, 1, 2, -1, -10, 10], 'hrs'),
            ('hours',   [0, 1, 2, -1, -10, 10], 'hour'),
            ('hours',   [0, 1, 2, -1, -10, 10], 'hours'),
            ('minutes', [0, 1, 2, -1, -10, 10], 'm'),
            ('minutes', [0, 1, 2, -1, -10, 10], 'min'),
            ('minutes', [0, 1, 2, -1, -10, 10], 'mins'),
            ('minutes', [0, 1, 2, -1, -10, 10], 'minute'),
            ('minutes', [0, 1, 2, -1, -10, 10], 'minutes'),
            ('seconds', [0, 1, 2, -1, -10, 10], 's'),
            ('seconds', [0, 1, 2, -1, -10, 10], 'sec'),
            ('seconds', [0, 1, 2, -1, -10, 10], 'secs'),
            ('seconds', [0, 1, 2, -1, -10, 10], 'second'),
            ('seconds', [0, 1, 2, -1, -10, 10], 'seconds '),
        ]

        # for each value in each test, check to make sure a string formatted
        # with the value + suffix (with and without a space separator)
        # returns the value for the key in the output
        for key, values, suffix in tests:
            for v in values:
                # test without a separator, ala '5d'
                input_string = '{}{}'.format(v, suffix)
                self.assertEqual(v, util.tdelta(input_string).get(key), '{} != {}'.format(input_string, v))

                # test with a separator, ala '5 days'
                input_string = '{} {}'.format(v, suffix)
                self.assertEqual(v, util.tdelta(input_string).get(key), '{} != {}'.format(input_string, v))
                
                # test with other text
                input_string = 'hello {} {} world'.format(v, suffix)
                self.assertEqual(v, util.tdelta(input_string).get(key), '{} != {}'.format(input_string, v))

                # test with a + prefix, ala '+5d' or '+-10 days'
                input_string = '+{}{}'.format(v, suffix)
                self.assertEqual(v, util.tdelta(input_string).get(key), '{} != {}'.format(input_string, v))
