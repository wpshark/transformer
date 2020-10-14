# -*- coding: utf-8 -*-
import re
from transformer.registry import register
from transformer.transforms.base import BaseTransform

# Regex based on Kristie's regex here: https://regex101.com/r/1bsTTG/47
URL_REGEX_ALL = r"(?:\+?\d{8}(?:\d{1,5})?|\(\+?\d{2,3}\)\s?(?:\d{4}[\s*.-]?\d{4}|\d{3}[\s*.-]?\d{3,4}|\d{2}([\s*.-]?)\d{2}\1\d{2}(?:\1\d{2})?))|((\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4})|\(?\+?\d{1,3}?\)?[-.\s*]?\(?\d{1,3}?\)?[-.\s*]([-.\s*]?\d{1,9}){3,6}"
URL_REGEX_NA = r"((\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4})"
URL_REGEX_IN = r"(?:\+?\d{8}(?:\d{1,5})?|\(\+?\d{2,3}\)\s?(?:\d{4}[\s*.-]?\d{4}|\d{3}[\s*.-]?\d{3,4}|\d{2}([\s*.-]?)\d{2}\1\d{2}(?:\1\d{2})?))"

class StringPhoneExtractV2Transform(BaseTransform):

    category = 'string'
    name = 'phone_extract_v2'
    label = 'Extract Phone Number'
    help_text = 'Find and copy a complete phone number out of a text field. Finds the first phone number only.'
    
    noun = 'Text'
    verb = 'find and copy a phone number from'

    def transform(self, str_input, regex='all', **kwargs):
        if isinstance(str_input, basestring):
            if regex=='na':
                match = re.search(URL_REGEX_NA, str_input)
                return match.group(0) if match else u''
            if regex=='in':
                match = re.search(URL_REGEX_IN, str_input)
                return match.group(0) if match else u''
            else:
                match = re.search(URL_REGEX_ALL, str_input)
                return match.group(0) if match else u''
        else:
            return u''

    def fields(self, *args, **kwargs):
        return [
            {
                "type": "unicode",
                "required": False,
                "key":  "regex",
                "choices": "all|All Formats,na|North American Number Plan,in|International Format (Standard)",
                "label": "Phone Number Format",
                "default": "all",
                "help_text": (
                    'By default, we\'ll use the most aggressive search, which could produce false positives. '
                    'If you find this, you can try the other options, or if numbers can\'t be found consistently, ' 
                    'try the [Extract Pattern](https://zapier.com/help/create/format/find-text-with-regex-in-zaps) transform.'),
         
            },
        ]


register(StringPhoneExtractV2Transform())
