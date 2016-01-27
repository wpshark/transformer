from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringReplaceTransform(BaseTransform):

    category = 'string'
    name = 'replace'
    label = 'Replace'
    help_text = 'Replace any character, word or phrase in the text with another character, word or phrase'

    def transform(self, str_input, str_old, str_new=u'', **kwargs):
        return str_input.replace(str_old, str_new) if str_input and str_old else u''

register(StringReplaceTransform())
