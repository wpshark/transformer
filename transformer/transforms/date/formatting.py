import arrow

from transformer.registry import register
from transformer.util import try_parse_date
from transformer.transforms.base import BaseTransform

class DateFormattingTransform(BaseTransform):

    category = 'date'
    name = 'formatting'
    label = 'Date / Formatting'
    help_text = 'Format a date into a specific format.'

    def transform(self, date_value, data=None, **kwargs):
        if data is None:
            data = {}

        from_format = data.get('from_format', '')
        to_format = data.get('to_format', '')

        dt = try_parse_date(date_value, from_format=from_format)
        if not dt:
            return self.raise_exception('Date could not be parsed')

        return arrow.get(dt).to('utc').format(to_format)

    def fields(self, *args, **kwargs):
        # Mon Jan 2 15:04:05 MST 2006

        dt = arrow.get(try_parse_date('Mon Jan 2 15:04:05 -0800 2006')).to('utc')

        formats = [
            'ddd DDD d HH:mm:ss Z YYYY',
            'MMMM DD YYYY HH:mm:ss',
            'MMMM DD YYYY',
            'MMM DD YYYY',
            'YYYY-MM-DD HH:mm:ss Z',
            'YYYY-MM-DD',
            'MM-DD-YYYY',
            'MM/DD/YYYY',
            'DD/MM/YY'
        ]

        choices = ','.join(['{}|{} ({})'.format(f, f, dt.format(f)) for f in formats])

        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'to_format',
                'choices': choices,
                'help_text': 'Provide the format that the date should be converted to.'
            }
        ]

register(DateFormattingTransform())
