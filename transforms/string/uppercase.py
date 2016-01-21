from registry import register
from transforms.base import BaseTransform

class StringUppercaseTransform(BaseTransform):

    def transform(self, str_input, **kwargs):
        return str_input.upper()

register('string.uppercase', StringUppercaseTransform())
