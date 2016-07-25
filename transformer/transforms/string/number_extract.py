from transformer.registry import register
from transformer.transforms.base import BaseTransform
import re

class StringNumberExtractTransform(BaseTransform):

    category = 'string'
    name = 'number_extract'
    label = 'Extract Number'
    help_text = 'Find and copy a number in text.'

    noun = 'Text'
    verb = 'find and copy a number from'

    def transform(self, str_input, **kwargs):
        if not str_input:
            return u''

        match = re.search(r'[-+]?[\d,]+[\.]?\d*', str_input)
        return match.group(0) if match else u''


register(StringNumberExtractTransform())
