import transformer.util as util

import unittest

class TestApp(unittest.TestCase):
    def test_util_tdelta(self):
        self.assertEqual(5, util.tdelta('5 years').get('years'))
        self.assertEqual(5, util.tdelta('5 years 3 months').get('years'))
        self.assertEqual(3, util.tdelta('5 years 3 months').get('months'))
        self.assertEqual(1, util.tdelta('5 years 3 months 1 second').get('seconds'))
        self.assertEqual(4, util.tdelta('5 years 3 months 1 second 4 minutes').get('minutes'))
        self.assertEqual(-2, util.tdelta('5 years -3 months 1 seconds 4 minutes -2 months').get('months'))
        self.assertEqual(1, util.tdelta('-+ 1 day - 1 week').get('days'))
        self.assertEqual(-1, util.tdelta('-+ 1 day - 1 week').get('weeks'))
