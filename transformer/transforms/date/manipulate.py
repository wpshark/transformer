import arrow

from transformer.registry import register
from transformer.util import try_parse_date, tdelta
from transformer.transforms.base import BaseTransform

class DateManipulateTransform(BaseTransform):

    category = 'date'
    name = 'manipulate'
    label = 'Date / Formatting'
    help_text = 'Manipulate a date and time by adding or subtracting '
    'days, months, years, hours, minutes, or seconds.'

    def transform(self, date_value, expression='', to_format='', **kwargs):
        delta = tdelta(expression)

        dt = try_parse_date(date_value)
        if not dt:
            return self.raise_exception('Date could not be parsed')

        return arrow.get(dt).to('utc').replace(**delta).format(to_format)

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'expression',
                'help_text': 'Provide the amount of time you would like to add to the date (negative values subtracts time).'
            },
            {
                'type': 'unicode',
                'required': True,
                'key': 'to_format',
                'help_text': 'Provide the format that the date should be converted to.'
            }
        ]

register(DateManipulateTransform())
