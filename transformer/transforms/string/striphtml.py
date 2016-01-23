from transformer.registry import register
from transformer.transforms.base import BaseTransform
import re

class StringStripHtmlTransform(BaseTransform):

    category = 'string'
    name = 'strip html'
    label = 'String / Strip HTML'
    help_text = 'Remove every HTML tag to leave just the plain text.'

    def transform(self, str_input, **kwargs):
        return re.sub("<.*?>", "", str_input) if str_input else ''

register(StringStripHtmlTransform())
