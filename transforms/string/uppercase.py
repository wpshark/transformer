from registry import register
from transforms.base import BaseTransform

class StringUppercaseTransform(BaseTransform):

    name = 'Uppercase'

    def transform(self, str_input, **kwargs):
        return str_input.upper() if str_input else ''

register('string.uppercase', StringUppercaseTransform())
