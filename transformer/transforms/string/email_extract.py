import re
from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringEmailExtractTransform(BaseTransform):

    category = 'string'
    name = 'email_extract'
    label = 'Extract Email Address'
    help_text = 'Find and copy an email address out of a text field. Finds the first email address only.'

    noun = 'Text'
    noun_plural = 'Text'
    verb = 'find and copy an email address from'

    def transform(self, str_input, **kwargs):
        if isinstance(str_input, basestring):
            match = re.search(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', str_input)
            return match.group(0) if match else u''
        else:
            return u''


register(StringEmailExtractTransform())
