# -*- coding: utf-8 -*-
import re
from transformer.registry import register
from transformer.transforms.base import BaseTransform

# Regex based on Kristie's regex here: https://regex101.com/r/1bsTTG/47
URL_REGEX = r"(?:\+?\d{8}(?:\d{1,5})?|\(\+?\d{2,3}\)\s?(?:\d{4}[\s*.-]?\d{4}|\d{3}[\s*.-]?\d{3,4}|\d{2}([\s*.-]?)\d{2}\1\d{2}(?:\1\d{2})?))|((\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4})|\(?\+?\d{1,4}?\)?[-.\s]?\(?\d{1,3}?\)?([-.\s]?\d{1,9}){3,6}"


class StringPhoneExtractV2Transform(BaseTransform):

    category = 'string'
    name = 'phone_extract_v2'
    label = 'Extract Phone Number'
    help_text = 'Find and copy a complete phone number out of a text field. Finds the first phone number only.'

    noun = 'Text'
    verb = 'find and copy a phone number from'

    def transform(self, str_input, **kwargs):
        if isinstance(str_input, basestring):
            match = re.search(URL_REGEX, str_input)
            return match.group(0) if match else u''
        else:
            return u''


register(StringPhoneExtractV2Transform())
