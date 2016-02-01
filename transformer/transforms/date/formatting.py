import arrow

from transformer.registry import register
from transformer.util import try_parse_date
from transformer.transforms.base import BaseTransform

class DateFormattingTransform(BaseTransform):

    category = 'date'
    name = 'formatting'
    label = 'Format'
    help_text = 'Change a date or time to a new format or style'

    def transform(self, date_value, from_format=u'', to_format=u'', **kwargs):
        dt = try_parse_date(date_value, from_format=from_format)
        if not dt:
            return self.raise_exception('Date could not be parsed')

        return arrow.get(dt).to('utc').format(to_format)

    def fields(self, *args, **kwargs):
        dt = arrow.get(try_parse_date('Mon Jan 22 15:04:05 -0800 2006')).to('utc')

        formats = [
            'ddd MMM DDD HH:mm:ss Z YYYY',
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
                'help_text': 'Provide the format that the date is converted to.'
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'from_format',
                'choices': choices,
                'help_text': 'If we incorrectly interpret the incoming (input) date, set this to explicitly tell us the format. Otherwise, we will do our best to figure it out.'
            }
        ]

register(DateFormattingTransform())
