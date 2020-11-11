import arrow

from transformer.registry import register
from transformer.util import try_parse_date, tdelta, shift_date
from transformer.transforms.base import BaseTransform
from transformer.transforms.date.formatting import PREDEFINED_DATE_FORMATS

class DateManipulateTransform(BaseTransform):

    category = 'date'
    name = 'manipulate'
    label = 'Add/Subtract Time'
    help_text = 'Manipulate a date and/or time by adding/subtracting days, months, years, hours, minutes, seconds.'

    noun = 'Date'
    verb = 'manipulate'

    def transform(self, date_value, expression='', from_format='', to_format='', **kwargs):
        if date_value is None:
            date_value = ''

        delta = tdelta(expression)

        dt = try_parse_date(date_value, from_format=from_format)
        if not dt:
            return self.raise_exception('Date could not be parsed')

        dt = shift_date(dt, delta)
        if not dt:
            return self.raise_exception('Date could not be manipulated')

        return arrow.get(dt).to('utc').format(to_format)


    def fields(self, *args, **kwargs):
        dt = arrow.get(try_parse_date('Mon Jan 22 15:04:05 -0800 2006')).to('utc')

        format_choices = ','.join(['{}|{} ({})'.format(f, f, dt.format(f)) for f in PREDEFINED_DATE_FORMATS])

        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'expression',
                'help_text': (
                    'Provide the amount of time you would like to add or subtract to the date (negative values subtract time). '
                    'Examples: `+8 hours 1 minute`, `+1 month -2 days`, `-1 day +8 hours`.'
                )
            },
            {
                'type': 'unicode',
                'required': True,
                'key': 'to_format',
                'choices': format_choices,
                'help_text': 'Provide the format that the date should be converted to. For date format help, see: https://zapier.com/help/create/format/modify-date-formats-in-zaps#customize-date-time-options'
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'from_format',
                'choices': format_choices,
                'help_text': 'If we incorrectly interpret the incoming (input) date, set this to explicitly tell us the format. Otherwise, we will do our best to figure it out.' # NOQA
            },
        ]

register(DateManipulateTransform())
