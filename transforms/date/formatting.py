import arrow
import datetime
import dateutil.parser

from registry import register
from transforms.base import BaseTransform

class DateFormattingTransform(BaseTransform):

    category = 'date'
    name = 'formatting'
    label = 'Date / Formatting'
    help_text = 'Format a date into a specific format.'

    def try_parse(self, date_value, from_format=None):
        """
        try to parse a int or string value into a datetime format

        """
        try:
            # check to see if the string can be converted into a float (a timestamp)
            try:
                date_value = float(date_value)
            except:
                pass

            # if this is a unix string... or a milliseconds since epoch
            if isinstance(date_value, int) or isinstance(date_value, long) or isinstance(date_value, float):
                if date_value >= (1 << 32) - 1:
                    date_value /= 1000.0
                return datetime.datetime.fromtimestamp(date_value)

            # otherwise, try to parse the date value from the from_format
            if from_format:
                dt = arrow.get(date_value, from_format)
                if dt:
                    return dt
        except:
            pass

        # otherwise, use the fuzzy parser
        return dateutil.parser.parse(date_value, fuzzy=True)

    def transform(self, date_value, data=None, **kwargs):
        if data is None:
            data = {}

        from_format = data.get('from_format', '')
        to_format = data.get('to_format', '')

        dt = self.try_parse(date_value, from_format=from_format)
        if not dt:
            return self.raise_exception('Date could not be parsed')

        return arrow.get(dt).to('utc').format(to_format)

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
                'key': 'from_format',
                'help_text': 'Optionally provide the format that the date is coming from (especially useful for uncommon strings)'
            },
            {
                'type': 'unicode',
                'required': True,
                'key': 'to_format',
                'help_text': 'Provide the format that the date should be converted to.'
            }
        ]

register(DateFormattingTransform())
