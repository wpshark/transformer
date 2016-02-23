from transformer.registry import register
from transformer.transforms.base import BaseTransform


class UtilLookupTransform(BaseTransform):

    category = 'util'
    name = 'lookup'
    label = 'Lookup Table'
    help_text = 'Given a key and table - find the corresponding value.'

    noun = 'Value'
    verb = 'lookup in'

    def build_input_field(self):
        return {
            'type': 'dict',
            'required': False,
            'key': 'table',
            'label': 'Lookup Table',
            'help_text': 'The table that will be used for the lookup - keys on the left and values on the right.',
        }

    def transform(self, table, key=u'', fallback=u'', **kwargs):
        if key and key in table:
            return table[key]
        return fallback

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
                'key': 'key',
                'label': 'Lookup Key',
                'help_text': 'Given this key, look for a corresponding value in the Lookup Table.'
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'fallback',
                'label': 'Fallback Value',
                'help_text': 'The value to be used if we do not find a corresponding value in Lookup Table.'
            }
        ]

register(UtilLookupTransform())
