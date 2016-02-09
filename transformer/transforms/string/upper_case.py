from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringUppercaseTransform(BaseTransform):

    category = 'string'
    name = 'upper_case'
    label = 'Uppercase'
    help_text = 'Capitalize every character in the text'

    noun = 'Text'
    noun_plural = 'Text'
    verb = 'capitalize every character'

    def transform(self, str_input, **kwargs):
        return str_input.upper() if str_input else u''

register(StringUppercaseTransform())
