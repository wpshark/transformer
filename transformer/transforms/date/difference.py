import arrow
import datetime

from transformer.registry import register
from transformer.util import try_parse_date, tdelta, shift_date
from transformer.transforms.base import BaseTransform
from transformer.transforms.date.formatting import PREDEFINED_DATE_FORMATS

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

class DateDifferenceTransform(BaseTransform):

    category = 'date'
    name = 'difference'
    label = 'Calculate Time Between Two Dates'
    help_text = 'Calculate the time between two given dates.'

    noun = 'Date'
    verb = 'difference'

    def transform(self, date_value, expression=u'', from_format=u'', to_format=u'', unit=u'', second_date=u'', **kwargs):
        if date_value is None:
            date_value = u''
        # first input = date 1
        # second input = date 2
        # we want to subtract date 1 from date 2

        delta = tdelta(expression)

        date_1 = try_parse_date(date_value, from_format=from_format)
        date_2 = try_parse_date(second_date, from_format=from_format)

        if not date_1 or not date_2:
            return self.raise_exception('Date could not be parsed')
        

        return {'id': 'erin is great'}


    def fields(self, *args, **kwargs):
        dt = arrow.get(try_parse_date('Mon Jan 22 15:04:05 -0800 2006')).to('utc')

        format_choices = ','.join(['{}|{} ({})'.format(f, f, dt.format(f)) for f in PREDEFINED_DATE_FORMATS])

        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'second_date',
                'help_text': '',
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'unit',
                'choices': ['milliseconds', 'seconds', 'hours', 'days'],
                'help_text': '',
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'from_format',
                'choices': format_choices,
                'help_text': 'If we incorrectly interpret the incoming (input) date, set this to explicitly tell us the format. Otherwise, we will do our best to figure it out.' # NOQA
            },
        ]

register(DateDifferenceTransform())
