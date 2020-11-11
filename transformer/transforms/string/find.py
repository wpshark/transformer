from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number


class StringFindTransform(BaseTransform):

    category = 'string'
    name = 'find'
    label = 'Find'
    help_text = 'Find the first position of a value in the text, -1 if the value is not found'

    noun = 'Text'
    verb = 'Search'

    def transform(self, str_input, find='', offset=0, **kwargs):
        str_input = str_input or ''
        find = find or ''
        pos = -1

        if isinstance(offset, str):
            offset = try_parse_number(offset, cls=int, default=None)

        if not isinstance(offset, int):
            self.raise_exception('offset must be a number')

        if str_input and find:
            pos = str_input.find(find, offset)

        return pos

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
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
