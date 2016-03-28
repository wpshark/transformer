from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import expand_special_chargroups

class StringReplaceTransform(BaseTransform):

    category = 'string'
    name = 'replace'
    label = 'Replace'
    help_text = 'Replace any character, word or phrase in the text with another character, word or phrase'

    noun = 'Text'
    verb = 'find and replace values within'

    def transform(self, str_input, old, new=u'', **kwargs):
        if old:
            old = expand_special_chargroups(old)
        if new:
            new = expand_special_chargroups(new)
        return str_input.replace(old, new) if str_input and old else u''

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'old',
                'label': 'Find',
                'help_text': 'To find a space, use `[:space:]`. For supported special characters, see: https://zapier.com/help/formatter/#special-characters'
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'new',
                'label': 'Replace',
                'help_text': 'Leave blank to delete the found text'
            },
        ]

register(StringReplaceTransform())
