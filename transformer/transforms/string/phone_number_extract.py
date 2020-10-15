# -*- coding: utf-8 -*-
import re
from transformer.registry import register
from transformer.transforms.base import BaseTransform

# Regex based on second script in question here (https://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script)
# Tweaked to accept international phone numbers, including 2 digit country codes and area codes, along with area codes that begin with a 0: https://gist.github.com/maguay/f3a46f578568a608413530e27b78af88
# updated to include seperate regexes - testing done at https://regex101.com/r/1bsTTG/51
URL_REGEX_ORIG = r"""(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?"""
URL_REGEX_ALL = r"(?:\+?\d{8}(?:\d{1,5})?|\(\+?\d{2,3}\)\s?(?:\d{4}[\s*.-]?\d{4}|\d{3}[\s*.-]?\d{3,4}|\d{2}([\s*.-]?)\d{2}\1\d{2}(?:\1\d{2})?))|((\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4})|\(?\+?\d{1,3}?\)?[-.\s*]?\(?\d{1,3}?\)?[-.\s*]([-.\s*]?\d{1,9}){3,6}"
URL_REGEX_NA = r"(?:\+?\d{10,11}?(?=\s)|(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4})"
URL_REGEX_IN = r"(?:\+?\d{8}(?:\d{1,5})?|\(\+?\d{2,3}\)\s?(?:\d{4}[\s*.-]?\d{4}|\d{3}[\s*.-]?\d{3,4}|\d{2}([\s*.-]?)\d{2}\1\d{2}(?:\1\d{2})?))"


class StringPhoneExtractTransform(BaseTransform):

    category = 'string'
    name = 'phone_extract'
    label = 'Extract Phone Number'
    help_text = 'Find and copy a complete phone number out of a text field. Finds the first phone number only.'
    
    noun = 'Text'
    verb = 'find and copy a phone number from'

    def transform(self, str_input, regex='orig', **kwargs):
        if isinstance(str_input, basestring):
            if regex=='orig':
                match = re.search(URL_REGEX_ORIG, str_input)
                return match.group(0) if match else u''
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
                "choices": "orig|Original (Most NANP and International),na|North American Number Plan (NANP),in|International,all|All Formats,",
                "label": "Phone Number Format",
                "default": "orig",
                "help_text": (
                    'By default, we\'ll use our original search, which is good for most NANPs and many International numbers. '
                    'If you find this does not work, you can try the other options for a specific format (NAMP and International), ' 
                    'or "All", which will find most numbers, but also can result in false positives.')
         
            },
        ]


register(StringPhoneExtractTransform())
