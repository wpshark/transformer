from transformer.registry import register
from transformer.transforms.base import BaseTransform


class StringDefaultValueTransform(BaseTransform):

    category = 'string'
    name = 'default_value'
    label = 'Default Value'
    help_text = 'Return a default value if the text is empty.'

    noun = 'Text'
    verb = 'check if empty'

    def transform(self, str_input, default_value=u'', **kwargs):
        return str_input if str_input is not None and str_input != "" else default_value

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'default_value',
                'label': 'Default Value',
                'help_text': 'Value to return if the text is empty.'
            }
        ]


register(StringDefaultValueTransform())
