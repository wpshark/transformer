from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringTruncateTransform(BaseTransform):

    category = 'string'
    name = 'truncate'
    label = 'String / Truncate'
    help_text = 'Limit your text to a specific character length, and delete anything over that.'

    def transform(self, str_input, **kwargs):
        return str_input.strip() if str_input else ''

register(StringTruncateTransform())
