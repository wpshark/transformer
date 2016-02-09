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
