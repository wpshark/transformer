import urllib.request, urllib.parse, urllib.error

from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringURLDecodeTransform(BaseTransform):

    category = 'string'
    name = 'url_decode'
    label = 'URL Decode'
    help_text = 'Decodes text from URLs.'

    noun = 'Text'
    verb = 'decode'

    def transform(self, str_input, use_plus=False, **kwargs):
        if not str_input:
            return ''

        if use_plus:
            decoded_text = urllib.parse.unquote_plus(str_input)
        else:
            decoded_text = urllib.parse.unquote(str_input)

        return decoded_text

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'bool',
                'required': False,
                'key': 'use_plus',
                'label': 'Convert plus to spaces?',
                'help_text': 'Will convert "+" to spaces instead of converting "%20", and will _not_ convert "/".',
            },
        ]

register(StringURLDecodeTransform())
