import unittest
import formatting

class TestDateFormattingTransform(unittest.TestCase):
    def test_from_to_format(self):
        transformer = formatting.DateFormattingTransform()
        self.assertEqual(transformer.transform(
            '2016-01-01',
            from_format='YYYY-MM-DD',
            to_format='MMMM DD, YYYY'
        ), "January 01, 2016")

    def test_fuzzy_to_format(self):
        transformer = formatting.DateFormattingTransform()
        self.assertEqual(transformer.transform(
            'I ordered it on January 17, 2047 ok?',
            to_format='MM-DD-YYYY'
        ), "01-17-2047")

    def test_fuzzy_relative_to_format(self):
        transformer = formatting.DateFormattingTransform()
        self.assertNotEqual(transformer.transform(
            'next friday',
            to_format='MM-DD-YYYY'
        ), "")

    def test_parse_timestamp(self):
        transformer = formatting.DateFormattingTransform()
        self.assertEqual(transformer.transform(
            1453498140,
            to_format='MM-DD-YYYY'
        ), "01-22-2016")

        self.assertEqual(transformer.transform(
            1453498140000,
            to_format='MM-DD-YYYY'
        ), "01-22-2016")

        self.assertEqual(transformer.transform(
            1453498140.001,
            to_format='MM-DD-YYYY'
        ), "01-22-2016")

        self.assertEqual(transformer.transform(
            '1453498140',
            to_format='MM-DD-YYYY'
        ), '01-22-2016')

        self.assertEqual(transformer.transform(
            '1453498140000',
            to_format='MM-DD-YYYY'
        ), '01-22-2016')

        self.assertEqual(transformer.transform(
            '1453498140.001',
            to_format='MM-DD-YYYY'
        ), '01-22-2016')
