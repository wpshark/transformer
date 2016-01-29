from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringNumberExtractTransform(BaseTransform):

    category = 'string'
    name = 'number_extract'
    label = 'Extract Number'
    help_text = 'Find and copy a number in text.'


    def transform(self, str_input, **kwargs):
        if not str_input:
            return u''

        num = u''.join([x for x in str_input if x in u'1234567890-., '])
        return num.strip()


register(StringNumberExtractTransform())
