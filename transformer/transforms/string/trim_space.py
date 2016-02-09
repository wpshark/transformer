from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringTrimSpaceTransform(BaseTransform):

    category = 'string'
    name = 'trim_space'
    label = 'Trim Whitespace'
    help_text = 'Removes leading and trailing whitespace.'

    noun = 'Text'
    noun_plural = 'Text'
    verb = 'remove leading and trailing whitespace from'

    def transform(self, str_input, **kwargs):
        return str_input.strip() if str_input else u''

register(StringTrimSpaceTransform())
