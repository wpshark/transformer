import unittest
import manipulate

class TestDateManipulateTransform(unittest.TestCase):
    def test_basic_manipulate(self):
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
