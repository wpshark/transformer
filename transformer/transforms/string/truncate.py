from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringTruncateTransform(BaseTransform):

    category = 'string'
    name = 'truncate'
    label = 'Truncate'
    help_text = 'Limit your text to a specific character length, and delete anything over that.'

    noun = 'Text'
    verb = 'truncate'

    def transform(self, str_input, offset=0, max_length=None, append_ellipsis=False, **kwargs):
        if max_length is None:
            max_length = len(str_input or u'')
        if not str_input or max_length <= 0:
            return u''

        short_text = str_input[offset:max_length]

        if append_ellipsis:
            short_text = short_text[0:-3] + u'...'

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
                'type': 'int',
                'required': False,
                'key': 'offset',
                'label': 'Skip Characters',
                'help_text': 'Will skip the first N characters in the text.'
            },
            {
                'type': 'bool',
                'required': False,
                'key': 'append_ellipsis',
                'label': 'Append Ellipsis?',
                'help_text': 'Will shorten text by three characters and append "..." to the end.'
            }
        ]

register(StringTruncateTransform())
