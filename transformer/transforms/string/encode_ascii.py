from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringEncodeasciiTransform(BaseTransform):

    category = 'string'
    name = 'encode_ascii'
    label = 'Convert to ASCII'
    help_text = 'Removes all non-ASCII characters.'

    noun = 'Text'
    verb = 'convert to ASCII'

    def transform(self, str_input, **kwargs):
        return str_input.encode('ascii', 'ignore') if str_input else u''

register(StringEncodeasciiTransform())
