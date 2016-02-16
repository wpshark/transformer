from transformer.registry import register
from transformer.transforms.base import BaseTransform

import re
import phonenumbers

class PhoneNumberFormattingTransform(BaseTransform):

    category = 'number'
    name = 'phone'
    label = 'Format Phone Number'
    help_text = 'Format a phone number to a new style.'

    noun = 'Phone Number'
    verb = 'format to a new style'

    def transform(self, phone_string, format_string=u'', default_region=u'US', **kwargs):
        if phone_string is None:
            return u''

        number = phonenumbers.parse(phone_string, default_region)

        if not phonenumbers.is_possible_number(number) or not phonenumbers.is_valid_number(number):
            return u''

        try:
            format_int = int(format_string)
            if format_int in (4, 5): # we should be using international format for these...
                format_int = 1
        except:
            format_int = None

        output = phonenumbers.format_number(number, format_int)

        # if we're using the national format, ensure that the first group of numbers is always grouped by parens
        if format_string == '2':
            output = re.sub('^(\d+)\s', '(\\1) ', output)

        # if we're using rfc3699, remove the 'tel:' from the format
        if format_string == '3':
            output = output.replace('tel:', '')

        # if we're using International, No Country Code, remove the +## prefix
        if format_string == '4':
            output = re.sub('^[+]\d+\s', '', output)

        # if we're using International, No Hyphens, replace hyphens with spaces
        if format_string == '5':
            output = re.sub('-', ' ', output)

        return output


    def fields(self, *args, **kwargs):
        available_formats = {
            '0': '+15558001212 (E164)',
            '1': '+1 555-800-1212 (International)',
            '2': '(555) 800-1212 (National)',
            '3': '+1-555-800-1212 (RFC3966)',
            '4': '555-800-1212 (International, No Country Code)',
            '5': '+1 555 800 1212 (International, No Hyphens)',
        }

        return [
            {
                'key': 'format_string',
                'type': 'unicode',
                'label': 'To Format',
                'help_text': 'The format the phone number will be converted to.',
                'required': True,
                'choices': available_formats,
            }
        ]



register(PhoneNumberFormattingTransform())
