import urllib

from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringURLEncodeTransform(BaseTransform):

    category = 'string'
    name = 'url_encode'
    label = 'URL Encode'
    help_text = 'Encodes text for use in URLs.'

    noun = 'Text'
    verb = 'encode'

    def transform(self, str_input, use_plus=False, **kwargs):
        if not str_input:
            return u''

        if use_plus:
            encoded_text = urllib.quote_plus(str_input)
        else:
            encoded_text = urllib.quote(str_input)

        return encoded_text

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'bool',
                'required': False,
                'key': 'use_plus',
                'label': 'Convert space to plus?',
                'help_text': 'Will convert spaces to "+" instead of "%20" and will _not_ convert "/".',
            },
        ]

register(StringURLEncodeTransform())
