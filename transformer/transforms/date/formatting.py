import arrow

from transformer.registry import register
from transformer.util import try_parse_date
from transformer.transforms.base import BaseTransform

PREDEFINED_DATE_FORMATS = [
    'ddd MMM DDD HH:mm:ss Z YYYY',
    'MMMM DD YYYY HH:mm:ss',
    'MMMM DD YYYY',
    'MMM DD YYYY',
    'YYYY-MM-DDTHH:mm:ssZ',
    'YYYY-MM-DD HH:mm:ss Z',
    'YYYY-MM-DD',
    'MM-DD-YYYY',
    'MM/DD/YYYY',
    'MM/DD/YY',
    'DD-MM-YYYY',
    'DD/MM/YYYY',
    'DD/MM/YY'
]

class DateFormattingTransform(BaseTransform):

    category = 'date'
    name = 'formatting'
    label = 'Format'
    help_text = 'Change a date or time to a new format or style'

    noun = 'Date'
    verb = 'format'

    def transform(self, date_value, from_format=u'', to_format=u'', **kwargs):
        if not date_value:
            return date_value

        dt = try_parse_date(date_value, from_format=from_format)
        if not dt:
            return self.raise_exception('Date could not be parsed')

        return arrow.get(dt).to('utc').format(to_format)

    def fields(self, *args, **kwargs):
        dt = arrow.get(try_parse_date('Mon Jan 22 15:04:05 -0800 2006')).to('utc')

        choices = ','.join(['{}|{} ({})'.format(f, f, dt.format(f)) for f in PREDEFINED_DATE_FORMATS])

        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'to_format',
                'choices': choices,
                'help_text': 'Provide the format that the date is converted to. For date format help, see: https://zapier.com/help/formatter/#date-time'
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'from_format',
                'choices': choices,
                'help_text': 'If we incorrectly interpret the incoming (input) date, set this to explicitly tell us the format. Otherwise, we will do our best to figure it out.' # NOQA
            }
        ]

register(DateFormattingTransform())
