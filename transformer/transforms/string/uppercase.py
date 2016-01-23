from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringUppercaseTransform(BaseTransform):

    category = 'string'
    name = 'uppercase'
    label = 'String / Uppercase'
    help_text = 'Convert all characters in a string to uppercase'

    def transform(self, str_input, **kwargs):
        return str_input.upper() if str_input else ''

register(StringUppercaseTransform())
