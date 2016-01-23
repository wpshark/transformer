from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringCapitalizeTransform(BaseTransform):

    category = 'string'
    name = 'capitalize'
    label = 'String / Capitalize'
    help_text = 'Capitalize the first character of every word.'

    def transform(self, str_input, **kwargs):
        return str_input.title() if str_input else ''

register(StringCapitalizeTransform())
