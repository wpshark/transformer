from transformer.registry import register
from transformer.transforms.base import BaseTransform

import re


class StringLengthTransform(BaseTransform):

    category = 'string'
    name = 'length'
    label = 'Length'
    help_text = 'Count the number of characters in the text'

    noun = 'Text'
    verb = 'length'

    def transform(self, str_input, ignore_whitespace=False, **kwargs):
        str_input = str_input or ''
        if ignore_whitespace:
            str_input = re.sub('\W', '', str_input)
        return len(str_input)

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'bool',
                'required': False,
                'key': 'ignore_whitespace',
                'label': 'Ignore Whitespace?',
                'help_text': 'Will ignore whitespace characters, including tabs, spaces, and newlines.'
            }
        ]

register(StringLengthTransform())
