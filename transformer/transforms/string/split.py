from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number, expand_special_chargroups

class StringSplitTransform(BaseTransform):

    category = 'string'
    name = 'split'
    label = 'Split Text'
    help_text = 'Split the text on a character or word and return a segment'

    noun = 'String'
    verb = 'split'

    def transform(self, str_input, separator=u'', index=0, **kwargs):
        if not str_input:
            return u''

        separator = expand_special_chargroups(separator)

        if separator:
            segments = str_input.split(separator)
        else:
            segments = str_input.split()

        if index == 'all':
            return segments

        if index == 'fields':
            return { u'Item {}'.format(i + 1): s for i, s in enumerate(segments) }

        index = try_parse_number(index, cls=int)
        try:
            return segments[index]
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
                'help_text': 'Character or word separator to split the text on. (Default: `[:space:]`) For supported special characters, see: https://zapier.com/help/formatter/#special-characters)' # NOQA
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'index',
                'label': 'Segment Index',
                'help_text': 'Segment of text to return after splitting. (Default: First)',
                'choices': '0|First,1|Second,-1|Last,-2|Second to Last,all|All (as Line-items),fields|All (as Separate Fields)',
            },
        ]


register(StringSplitTransform())
