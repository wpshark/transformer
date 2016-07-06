import unittest
import datetime
from mock import patch

import formatting

class TestDateFormattingTransform(unittest.TestCase):
    transformer = formatting.DateFormattingTransform()

    def test_transforming_empty_field_returns_empty_field(self):
        self.assertEqual(self.transformer.transform(
            '',
            from_format='MM/DD/YYYY',
            to_format='YYYY-MM-DD'
        ), '')

        self.assertEqual(self.transformer.transform(
            None,
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
        self.assertEqual(self.transformer.transform(
            'I ordered it on January 17, 2047 ok?',
            to_format='MM-DD-YYYY'
        ), "01-17-2047")

        self.assertEqual(self.transformer.transform(
            'I ordered it on January 17, 2047 at 5PM ok?',
            to_format='MM-DD-YYYY HH:mm Z'
        ), "01-17-2047 17:00 -0000")

        self.assertEqual(self.transformer.transform(
            'I ordered it on January 17, 2047 at 5PM ok?',
            to_format='MM-DD-YYYY HH:mm Z',
            from_timezone='US/Eastern',
            to_timezone='US/Central'
        ), "01-17-2047 16:00 -0600")

    def test_fuzzy_relative_to_format(self):
        self.time = datetime.datetime(2016, 6, 17)
        class fakedatetime(datetime.datetime):
            @classmethod
            def now(cls):
                return self.time
            @classmethod
            def today(cls):
                return self.time
        patcher = patch('datetime.datetime', fakedatetime)
        patcher.start()

        tests = [
            ('sunday', '06-26-2016'),
            ('monday', '06-20-2016'),
            ('tuesday', '06-21-2016'),
            ('wednesday', '06-22-2016'),
            ('thursday', '06-23-2016'),
            ('friday', '06-24-2016'),
            ('saturday', '06-25-2016'),
        ]

        for day, date in tests:
            self.assertEqual(self.transformer.transform(
                'next %s' % day,
                to_format='MM-DD-YYYY'
            ), date)

        patcher.stop()

    def test_parse_timestamp(self):
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

    def test_change_timezone(self):
        # if no *input* timezone specified in the string, and no to_timezone is provided, both are assumed to be UTC
        self.assertEqual(self.transformer.transform(
            '22/01/2016 12:11:10',
            to_format='YYYY-MM-DD HH:mm:ss Z',
            from_format='MM/DD/YYYY HH:mm:ss',
        ), '2016-01-22 12:11:10 -0000')

        # if a timezone is specified in the string, and no to_timezone is provided, it assumed to be UTC
        self.assertEqual(self.transformer.transform(
            '22/01/2016 12:11:10 -0500',
            to_format='YYYY-MM-DD HH:mm:ss Z',
            from_format='MM/DD/YYYY HH:mm:ss',
        ), '2016-01-22 17:11:10 -0000')

        # if a timezone specified in the string, and a to_timezone is provided, convert between each
        self.assertEqual(self.transformer.transform(
            '22/01/2016 12:11:10 -0500',
            to_format='YYYY-MM-DD HH:mm:ss Z',
            from_format='MM/DD/YYYY HH:mm:ss',
            to_timezone='US/Central'
        ), '2016-01-22 11:11:10 -0600')

        # if both timezones are the same, no conversion occurs
        for Z, timezone in (
            ('-0500', 'US/Eastern'),
            ('-0500', '-05:00'),
            ('-0600', 'US/Central'),
            ('-0600', '-06:00'),
            ('-0700', 'US/Mountain'),
            ('-0700', '-07:00'),
            ('-0800', 'US/Pacific'),
            ('-0800', '-08:00')
        ):
            self.assertEqual(self.transformer.transform(
                '22/01/2016 12:11:10',
                to_format='YYYY-MM-DD HH:mm:ss Z',
                from_format='MM/DD/YYYY HH:mm:ss',
                from_timezone=timezone,
                to_timezone=timezone,
            ), '2016-01-22 12:11:10 {}'.format(Z))

        # if no *input* timezone specified in the string, it is assumed to be UTC unless specified
        self.assertEqual(self.transformer.transform(
            '22/01/2016 12:11:10',
            to_format='YYYY-MM-DD HH:mm:ss Z',
            from_format='MM/DD/YYYY HH:mm:ss',
            to_timezone='US/Pacific'
        ), '2016-01-22 04:11:10 -0800')

        # if no *input* timezone specified in the string check to make sure a specified one is used
        self.assertEqual(self.transformer.transform(
            '22/01/2016 12:11:10',
            to_format='YYYY-MM-DD HH:mm:ss Z',
            from_format='MM/DD/YYYY HH:mm:ss',
            from_timezone='US/Eastern',
            to_timezone='US/Pacific'
        ), '2016-01-22 09:11:10 -0800')

        # if an *input* timezone *is* specified in the string check to make sure a specified one is *not* used
        self.assertEqual(self.transformer.transform(
            '22/01/2016 12:11:10 -05:00',
            to_format='YYYY-MM-DD HH:mm:ss Z',
            from_format='MM/DD/YYYY HH:mm:ss',
            from_timezone='US/Central', # <-- this is IGNORED because the input string has a timezone specified
            to_timezone='US/Pacific'
        ), '2016-01-22 09:11:10 -0800')

        # if an *input* timezone *is* specified in the string check to make sure it stays used even if no from_timezone is provided
        self.assertEqual(self.transformer.transform(
            '22/01/2016 12:11:10 -05:00',
            to_format='YYYY-MM-DD HH:mm:ss Z',
            from_format='MM/DD/YYYY HH:mm:ss',
            to_timezone='US/Pacific'
        ), '2016-01-22 09:11:10 -0800')

    def test_all_timezones(self):
        import pytz

        prev = None
        for tz in pytz.all_timezones:
            # just make sure that the timezone conversion utc -> tz works...
            output = self.transformer.transform('22/01/2016 12:11:10 -05:00', to_format='YYYY-MM-DD HH:mm:ss Z', from_format='MM/DD/YYYY HH:mm:ss', to_timezone=tz) # NOQA
            self.assertTrue(output.startswith('2016-01-22') or output.startswith('2016-01-23'))

            if prev:
                # just make sure that the timezone conversion prev -> tz works...
                output = self.transformer.transform('22/01/2016 12:11:10', to_format='YYYY-MM-DD HH:mm:ss Z', from_format='MM/DD/YYYY HH:mm:ss', from_timezone=prev, to_timezone=tz) # NOQA
                self.assertTrue(output.startswith('2016-01-21') or output.startswith('2016-01-22') or output.startswith('2016-01-23'))

                # just make sure that the timezone conversion tz -> prev works...
                output = self.transformer.transform('22/01/2016 12:11:10', to_format='YYYY-MM-DD HH:mm:ss Z', from_format='MM/DD/YYYY HH:mm:ss', from_timezone=tz, to_timezone=prev) # NOQA
                self.assertTrue(output.startswith('2016-01-21') or output.startswith('2016-01-22') or output.startswith('2016-01-23'))

            prev = tz
