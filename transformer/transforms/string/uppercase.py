from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringUppercaseTransform(BaseTransform):

    category = 'string'
    name = 'uppercase'
    label = 'Uppercase'
    help_text = 'Capitalize every character in the text'

    def transform(self, str_input, **kwargs):
        return str_input.upper() if str_input else ''

register(StringUppercaseTransform())
