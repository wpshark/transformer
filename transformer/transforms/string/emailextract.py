import re
from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringEmailExtractTransform(BaseTransform):

    category = 'string'
    name = 'emailextract'
    label = 'Email Extract'
    help_text = 'Extract the first email address from an input'


    def transform(self, str_input, **kwargs):
        if isinstance(str_input, basestring):
            match = re.search(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', str_input)
            return match.group(0) if match else u''
        else:
            return u''


register(StringEmailExtractTransform())
