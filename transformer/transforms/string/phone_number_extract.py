# -*- coding: utf-8 -*-
import re
from transformer.registry import register
from transformer.transforms.base import BaseTransform


# updated to include seperate regexes - testing is much easier here:
# orig and default (UNI1): https://regex101.com/r/FCS4px/1
# uni2: https://regex101.com/r/sk6MVY/1
# na: https://regex101.com/r/QYWyPc/2
# in: https://regex101.com/r/DVkuoA/1

URL_REGEX_UNI1 = r"(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?"
URL_REGEX_UNI2 = r"(?:\+?\d{8}(?:\d{1,5})?|\(\+?\d{2,3}\)\s?(?:\d{4}[\s*.-]?\d{4}|\d{3}[\s*.-]?\d{3,4}|\d{2}([\s*.-]?)\d{2}\1\d{2}(?:\1\d{2})?))|((\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4})|\(?\+?\d{1,3}?\)?[-.\s*]?\(?\d{1,3}?\)?[-.\s*]([-.\s*]?\d{1,9}){3,6}"
URL_REGEX_NA = r"(?:\+1?\d{10}?(?=\s)|1\d{10}?(?=\s)|(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4})"
URL_REGEX_IN = r"(?:\+?\d{8}(?:\d{1,5})?|\(\+?\d{2,3}\)\s?(?:\d{4}[\s*.-]?\d{4}|\d{3}[\s*.-]?\d{3,4}|\d{2}([\s*.-]?)\d{2}\1\d{2}(?:\1\d{2})?))"


class StringPhoneExtractTransform(BaseTransform):

    category = 'string'
    name = 'phone_extract'
    label = 'Extract Phone Number'
    help_text = 'Find and copy a complete phone number out of a text field. Finds the first phone number only.'
    
    noun = 'Text'
    verb = 'find and copy a phone number from'

    def transform(self, str_input, regex='uni1', **kwargs):
        if isinstance(str_input, basestring):
            if regex=='uni2':
                match = re.search(URL_REGEX_UNI2, str_input)
                return match.group(0) if match else u''
            elif regex=='na':
                match = re.search(URL_REGEX_NA, str_input)
                return match.group(0) if match else u''
            elif regex=='in':
                match = re.search(URL_REGEX_IN, str_input)
                return match.group(0) if match else u''
            else:
                match = re.search(URL_REGEX_UNI1, str_input)
                return match.group(0) if match else u''
        else:
            return u''

    def fields(self, *args, **kwargs):
        return [
            {
                "type": "unicode",
                "required": False,
                "key":  "regex",
                "choices": "na|North American Number Plan (NANP) e.g. (123) 456-7890,in|International e.g. (12) 34-56-78-90,uni1|Universal 1 (includes NANP and some International),uni2|Universal 2 (includes NANP and more International)",
                "label": "Phone Number Format",
                "default": "uni1",
                "help_text": (
                    'By default, the **Universal 1** search is used, which will find many NANP and International numbers. '
                    'If this does not work consistently, try a specific format (**NAMP** or **International**), ' 
                    'or **Universal 2**, which will find most phone numbers, but can also result in false positives.')
         
            },
        ]


register(StringPhoneExtractTransform())
