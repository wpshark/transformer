from transformer.registry import register
from transformer.transforms.base import BaseTransform

class StringWordCountTransform(BaseTransform):

    category = 'string'
    name = 'word_count'
    label = 'Word Count'
    help_text = 'Count the number of words in a string.'

    noun = 'Text'
    verb = 'count'

    def transform(self, str_input, **kwargs):
        if not str_input:
            return 0

        # splits on space, tab, newline, return, formfeed
        return len(str_input.split())

register(StringWordCountTransform())
