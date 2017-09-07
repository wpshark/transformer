# -*- coding: utf-8 -*-
import re
from transformer.registry import register
from transformer.transforms.base import BaseTransform

# Regex based on second script in question here (https://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script)
# Tweaked to accept international phone numbers, including 2 digit country codes and area codes, along with area codes that begin with a 0: https://gist.github.com/maguay/f3a46f578568a608413530e27b78af88
URL_REGEX = r"""(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?"""


class StringPhoneExtractTransform(BaseTransform):

    category = 'string'
    name = 'phone_extract'
    label = 'Extract Phone Number'
    help_text = 'Find and copy a complete out of a text field. Finds the first phone number only.'

    noun = 'Text'
    verb = 'find and copy a phone number from'

    def transform(self, str_input, **kwargs):
        if isinstance(str_input, basestring):
            match = re.search(URL_REGEX, str_input)
            return match.group(0) if match else u''
        else:
            return u''


register(StringPhoneExtractTransform())
