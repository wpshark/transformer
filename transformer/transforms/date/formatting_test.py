import unittest
import formatting

class TestDateFormattingTransform(unittest.TestCase):
    def test_from_to_format(self):
        transformer = formatting.DateFormattingTransform()

        # Try an ambiguous date with a month then days format
        self.assertEqual(transformer.transform(
            '03/01/2016',
            from_format='MM/DD/YYYY',
            to_format='YYYY-MM-DD'
        ), '2016-03-01')

        # Flipping the format to days then months should yield a different output
        self.assertEqual(transformer.transform(
            '03/01/2016',
            from_format='DD/MM/YYYY',
            to_format='YYYY-MM-DD'
        ), '2016-01-03')

        # If the from format is clearly wrong, we'll do the correct thing
        self.assertEqual(transformer.transform(
            '22/01/2016',
            to_format='YYYY-MM-DD',
            from_format='MM/DD/YYYY'
        ), '2016-01-22')

        # TODO: Check a weird format
        # self.assertEqual(transformer.transform(
        #     '01022016',
        #     to_format='YYYY-MM-DD',
        #     from_format='DDMMYYYY'
        # ), '2016-02-01')

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
