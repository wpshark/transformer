from transformer.registry import register
from transformer.transforms.base import BaseTransform


class UtilLookupTransform(BaseTransform):

    category = 'util'
    name = 'lookup'
    label = 'Lookup Table'
    help_text = 'Given a key and table - find the matching value.'

    noun = 'Value'
    verb = 'lookup'

    def build_input_field(self):
        return {
            'type': 'unicode',
            'required': False,
            'key': 'inputs',
            'label': 'Lookup Key',
            'help_text': '{} you would like to {}.'.format(self.noun or 'Value', self.verb or 'transform')
        }

    def transform(self, input_key, table={}, fallback='', **kwargs):
        if input_key and input_key in table:
            return table[input_key]
        return fallback

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'dict',
                'required': False,
                'key': 'table',
                'label': 'Lookup Table',
                'help_text': 'The table that will be used for the lookup - keys on the left and values on the right.',
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'fallback',
                'label': 'Fallback Value',
                'help_text': 'The value to be used if we do not find a matching value in Lookup Table.'
            }
        ]

register(UtilLookupTransform())
