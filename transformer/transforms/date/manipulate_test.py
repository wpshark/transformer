import unittest
import manipulate
import datetime

class TestDateManipulateTransform(unittest.TestCase):
    def test_basic_manipulate(self):
        now = datetime.datetime.now()
        transformer = manipulate.DateManipulateTransform()
        self.assertEqual(transformer.transform(
            '2016-01-01',
            expression='+1 month - 1 day',
            to_format='MMMM DD, YYYY'
        ), "January 31, 2016")

        self.assertEqual(transformer.transform(
            '2016-01-01',
            expression='- 1 month - 1 day',
            to_format='MMMM DD, YYYY'
        ), "November 30, 2015")

        self.assertEqual(transformer.transform(
            '2016-01-01',
            expression='+ 1 year - 1 month - 1 day',
            to_format='MMMM DD, YYYY'
        ), "November 30, 2016")

        self.assertEqual(transformer.transform(
            '2016-02-01',
            expression='+ 1 month - 1 day',
            to_format='MMMM DD, YYYY'
        ), "February 29, 2016")

        self.assertEqual(transformer.transform(
            '2016-02-01',
            expression='',
            to_format='MMMM DD, YYYY'
        ), "February 01, 2016")

        self.assertEqual(transformer.transform(
            '',
            expression='',
            to_format='DD-MM-YYYY',
            from_format='DD-MM-YYYY'
        ), now.strftime('%d-%m-%Y'))

        self.assertEqual(transformer.transform(
            '1455043091',
            expression='',
            to_format='MMMM DD, YYYY HH:mm'
        ), 'February 09, 2016 18:38')

        self.assertEqual(transformer.transform(
            '1455043091',
            expression='+1d +1h +1m',
            to_format='MMMM DD, YYYY HH:mm'
        ), "February 10, 2016 19:39")

        # this will fail, because the day/month is ambiguous
        self.assertNotEqual(transformer.transform(
            '12-08-2016',
            expression='+1 month',
            to_format='DD-MM-YYYY',
        ), '12-09-2016')

        self.assertEqual(transformer.transform(
            '12-08-2016',
            expression='+1 month',
            to_format='DD-MM-YYYY',
            from_format='DD-MM-YYYY'
        ), '12-09-2016')

        self.assertEqual(transformer.transform(
            '23-08-2016',
            expression='+1 month',
            to_format='DD-MM-YYYY',
            from_format='DD-MM-YYYY'
        ), '23-09-2016')
