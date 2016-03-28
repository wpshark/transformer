import arrow
import dateutil.tz
import pytz

from transformer.registry import register
from transformer.util import try_parse_date
from transformer.transforms.base import BaseTransform

PREDEFINED_DATE_FORMATS = [
    'ddd MMM DD HH:mm:ss Z YYYY',
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

    def transform(self, date_value, from_format=u'', to_format=u'', from_timezone=u'', to_timezone=u'', **kwargs):
        if not date_value:
            return date_value

        if not to_timezone:
            to_timezone = u'UTC'

        dt = try_parse_date(date_value, from_format=from_format)
        if not dt:
            return self.raise_exception('Date could not be parsed')

        dtout = arrow.get(dt)

        # if the from_timezone is *not* UTC and our datetime *is* UTC, replace it...
        if from_timezone and from_timezone != 'UTC' and dtout.tzinfo == dateutil.tz.tzutc():
            dtout = dtout.replace(tzinfo=from_timezone)

        return dtout.to(to_timezone).format(to_format)

    def fields(self, *args, **kwargs):
        dt = arrow.get(try_parse_date('Mon Jan 22 15:04:05 -0800 2006')).to('utc')

        choices = ','.join(['{}|{} ({})'.format(f, f, dt.format(f)) for f in PREDEFINED_DATE_FORMATS])

        timezones = list(sorted(pytz.common_timezones, key=lambda v: '-' + v if v.startswith('US') else v))

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
                'key': 'to_timezone',
                'label': 'To Timezone',
                'choices': timezones,
                'default': 'UTC',
                'help_text': 'Choose a timezone the date should be converted to. (Default: UTC)'
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'from_timezone',
                'label': 'From Timezone',
                'choices': timezones,
                'default': 'UTC',
                'help_text': 'If no timezone is provided in the incoming (input) data, set this to explicitly tell us which to use. (Default: UTC)' # NOQA
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
