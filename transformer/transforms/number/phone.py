from transformer.registry import register
from transformer.transforms.base import BaseTransform

import re
import phonenumbers
from phonenumbers import NumberParseException

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

        try:
            number = phonenumbers.parse(phone_string, default_region)
        except NumberParseException:
            # Return original input if we can't do anything with it
            return phone_string

        if not phonenumbers.is_possible_number(number) or not phonenumbers.is_valid_number(number):
            return phone_string

        try:
            format_int = int(format_string)
            if format_int in (4, 5, 8): # we should be using international format for these...
                format_int = 1
            if format_int in (6, 7): # we should be using national format for these...
                format_int = 2
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

        # if we're using National, No Parens, remove the parens
        if format_string == '6':
            output = output.replace('(', '').replace(')', '')

        # if we're using symbols, remove symbols
        if format_string in ['7', '8']:
            output = output.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace('+', '')

        return output


    def fields(self, *args, **kwargs):
        available_formats = {
            '0': '+15558001212 (E164)',
            '1': '+1 555-800-1212 (International)',
            '2': '(555) 800-1212 (National)',
            '3': '+1-555-800-1212 (RFC3966)',
            '4': '555-800-1212 (International, No Country Code)',
            '5': '+1 555 800 1212 (International, No Hyphens)',
            '6': '555 800-1212 (National, No Parenthesis)',
            '7': '5558001212 (No Symbols, National)',
            '8': '15558001212 (No Symbols, International)',
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
