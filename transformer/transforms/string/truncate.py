from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringTruncateTransform(BaseTransform):

    category = 'string'
    name = 'truncate'
    label = 'Truncate'
    help_text = 'Limit your text to a specific character length, and delete anything over that.'

    def transform(self, str_input, max_length=-1, append_ellipsis=False, **kwargs):
        if not str_input or max_length <= 0:
            return ''

        short_text = str_input[0:max_length]

        if append_ellipsis and len(short_text) != len(str_input) and len(short_text) > 3:
            short_text = short_text[0:-3] + '...'

        return short_text

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'int',
                'required': True,
                'key': 'max_length',
                'help_text': 'The max length the text should be.'
            },
            {
                'type': 'bool',
                'required': False,
                'key': 'append_ellipsis',
                'label': 'Append Ellipsis?',
                'help_text': 'Will shorten text by three extra characters and append "..." to the end.'
            }
        ]

register(StringTruncateTransform())
