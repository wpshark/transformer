import arrow

from transformer.registry import register
from transformer.util import try_parse_date, tdelta, shift_date
from transformer.transforms.base import BaseTransform
from transformer.transforms.date.formatting import PREDEFINED_DATE_FORMATS

class DateDeltaTransform(BaseTransform):

    category = 'date'
    name = 'date_delta'
    label = 'Days Between Dates'
    help_text = 'Find the number of days between two dates.'

    # noun = 'Date'
    # verb = 'difference'

    def transform(self, first_date_value, second_date_value, **kwargs):
        return 'success!' + first_date_value + second_date_value 

    def fields(self, *args, **kwargs):
        dt = arrow.get(try_parse_date('Mon Jan 22 15:04:05 -0800 2006')).to('utc')
        
        format_choices = ','.join(['{}|{} ({})'.format(f, f, dt.format(f)) for f in PREDEFINED_DATE_FORMATS])
        
        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'first_date_value',
                'help_text': (
                    'Provide the first date here. The date format should be the same for both the dates.'
                    'Please note that we will always subtract date 2 from date 1. This date minus the below date.'
                )
            },
            {
                'type': 'unicode',
                'required': True,
                'key': 'second_date_value',
                'help_text': (
                    'Provide the second date here. The date format should be the same for both the dates.'
                    'Please note that we will always subtract date 2 from date 1. Above date minus this date.'
                )
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'format',
                'choices': format_choices,
                'help_text': 'If we incorrectly interpret any of the dates, set this to explicitly tell us the format. Otherwise, we will do our best to figure it out.'
            }
        ]

register(DateDeltaTransform())