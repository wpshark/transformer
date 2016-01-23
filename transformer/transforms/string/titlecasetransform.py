from titlecase import titlecase
from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringTitlecaseTransform(BaseTransform):

    category = 'string'
    name = 'titlecase'
    label = 'String / Titlecase'
    help_text = 'Convert all characters in a string to titlecase'

    def transform(self, str_input, **kwargs):
        return titlecase(str_input) if str_input else ''

register(StringTitlecaseTransform())
