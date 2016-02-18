from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number

class StringSplitTransform(BaseTransform):

    category = 'string'
    name = 'split'
    label = 'Split a String'
    help_text = 'Split a string and return a segment'

    noun = 'String'
    verb = 'split'

    def transform(self, str_input, separator=u'', segment=0, **kwargs):
        segment = try_parse_number(segment, cls=int)

        if separator:
            segments = str_input.split(separator)
        else:
            segments = str_input.split()

        try:
            return segments[segment]
        except:
            pass

        return u''

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
                'key': 'separator',
                'label': 'Separator',
                'help_text': 'Separator to split the string on. (Default: space)'
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'segment',
                'label': 'String segment to return after splitting',
                'choices': '0|First,1|Second,-1|Last,-2|Second to Last',
            },
        ]


register(StringSplitTransform())
