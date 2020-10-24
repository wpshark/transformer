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

    noun = 'Date'
    verb = 'subtract from'

    def transform(self, date_value, second_date_value, date_format=u'', **kwargs):
        if date_value is None:
            date_value = u''
        
        if second_date_value is None:
            second_date_value = u''

        dt1 = try_parse_date(date_value, from_format=date_format)
        if not dt1:
            return self.raise_exception('Date 1 could not be parsed')
        
        dt2 = try_parse_date(second_date_value, from_format=date_format)
        if not dt2:
            return self.raise_exception('Date 2 could not be parsed')
        
        delta = arrow.get(dt1) - arrow.get(dt2)

        days = delta.days

        return days

    def fields(self, *args, **kwargs):
        dt = arrow.get(try_parse_date('Mon Jan 22 15:04:05 -0800 2006')).to('utc')
        
        format_choices = ','.join(['{}|{} ({})'.format(f, f, dt.format(f)) for f in PREDEFINED_DATE_FORMATS])
        
        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'second_date_value',
                'help_text': (
                    'Provide the second date here. The date format should be the same for both the dates. '
                    'Please note that we will always subtract this date from the above date. '
                    'Above date minus this date.'
                )
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'date_format',
                'choices': format_choices,
                'help_text': 'If we incorrectly interpret any of the dates, set this to explicitly tell us the format. Otherwise, we will do our best to figure it out.'
            }
        ]

register(DateDeltaTransform())