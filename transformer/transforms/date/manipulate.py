import arrow

from transformer.registry import register
from transformer.util import try_parse_date, tdelta
from transformer.transforms.base import BaseTransform

class DateManipulateTransform(BaseTransform):

    category = 'date'
    name = 'manipulate'
    label = 'Add/Subtract Time'
    help_text = 'Manipulate a date and/or time by adding/subtracting days, months, years, hours, minutes, seconds.'

    noun = 'Date'
    verb = 'manipulate'

    def transform(self, date_value, expression=u'', to_format=u'', **kwargs):
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
                'help_text': (
                    'Provide the amount of time you would like to add or subtract to the date (negative values subtract time). '
                    'Examples: `+8 hours 1 minute`, `+1 month -2 days`, `-1 day +8 hours`.'
                )
            },
            {
                'type': 'unicode',
                'required': True,
                'key': 'to_format',
                'help_text': 'Provide the format that the date should be converted to. For date format help, see: https://zapier.com/help/formatter/#date-time'
            }
        ]

register(DateManipulateTransform())
