import unittest
import formatting

class TestDateFormattingTransform(unittest.TestCase):
    transformer = formatting.DateFormattingTransform()
    def test_transforming_empty_field_returns_empty_field(self):
        self.assertEqual(self.transformer.transform(
            '',
            from_format='MM/DD/YYYY',
            to_format='YYYY-MM-DD'
        ), '')

    def test_from_to_format(self):
        # Try an ambiguous date with a month then days format
        self.assertEqual(self.transformer.transform(
            '03/01/2016',
            from_format='MM/DD/YYYY',
            to_format='YYYY-MM-DD'
        ), '2016-03-01')

        # Flipping the format to days then months should yield a different output
        self.assertEqual(self.transformer.transform(
            '03/01/2016',
            from_format='DD/MM/YYYY',
            to_format='YYYY-MM-DD'
        ), '2016-01-03')

        # If the from format is clearly wrong, we'll do the correct thing
        self.assertEqual(self.transformer.transform(
            '22/01/2016',
            to_format='YYYY-MM-DD',
            from_format='MM/DD/YYYY'
        ), '2016-01-22')

    def test_fuzzy_to_format(self):
        self.transformer = formatting.DateFormattingTransform()
        self.assertEqual(self.transformer.transform(
            'I ordered it on January 17, 2047 ok?',
            to_format='MM-DD-YYYY'
        ), "01-17-2047")

    def test_fuzzy_relative_to_format(self):
        self.transformer = formatting.DateFormattingTransform()
        self.assertNotEqual(self.transformer.transform(
            'next friday',
            to_format='MM-DD-YYYY'
        ), "")

    def test_parse_timestamp(self):
        self.transformer = formatting.DateFormattingTransform()
        self.assertEqual(self.transformer.transform(
            1453498140,
            to_format='MM-DD-YYYY'
        ), "01-22-2016")

        self.assertEqual(self.transformer.transform(
            1453498140000,
            to_format='MM-DD-YYYY'
        ), "01-22-2016")

        self.assertEqual(self.transformer.transform(
            1453498140.001,
            to_format='MM-DD-YYYY'
        ), "01-22-2016")

        self.assertEqual(self.transformer.transform(
            '1453498140',
            to_format='MM-DD-YYYY'
        ), '01-22-2016')

        self.assertEqual(self.transformer.transform(
            '1453498140000',
            to_format='MM-DD-YYYY'
        ), '01-22-2016')

        self.assertEqual(self.transformer.transform(
            '1453498140.001',
            to_format='MM-DD-YYYY'
        ), '01-22-2016')

        # Including a from_format should prevent the usual timestamp parsing
        self.assertEqual(self.transformer.transform(
            '01022016',
            to_format='YYYY-MM-DD',
            from_format='MMDDYYYY'
        ), '2016-01-02')
