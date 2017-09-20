from transformer.registry import register
from transformer.transforms.base import BaseTransform


class StringFindTransform(BaseTransform):

    category = 'string'
    name = 'find'
    label = 'Find'
    help_text = 'Find the first position of a value in the text, -1 if the value is not found'

    noun = 'Text'
    verb = 'Find'

    def transform(self, str_input, find='', offset=0, **kwargs):
        str_input = str_input or u''
        find = find or u''
        pos = -1

        try:
            if str_input and find:
                pos = str_input.find(find, offset)
        except:
            pass

        return pos

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'find',
                'label': 'Find',
                'help_text': 'Value to find in the text'
            },
            {
                'type': 'int',
                'required': False,
                'key': 'offset',
                'label': 'Skip Characters',
                'help_text': 'Will skip the first N characters in the text.'
            },
        ]

register(StringFindTransform())
