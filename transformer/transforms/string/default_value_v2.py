from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import expand_special_chargroups


class StringDefaultValueV2Transform(BaseTransform):

    category = 'string'
    name = 'default_value_v2'
    label = 'Default Value'
    help_text = 'Return a default value if the text is empty. If a line-item field is provided, a line-item field is returned.'

    noun = 'Text'
    verb = 'check if empty'


    def get_defaulted_value(self, input, default_value):
        return input if input is not None and input != "" else expand_special_chargroups(default_value)

    def transform_many(self, inputs, options, **kwargs):
        # use transform_many as we need to know if the user passed an empty array
        # inputs can be a list, so test that out and replace values in a list (if we ever provide that): https://admin.zapier.com/rover/app/ZapierFormatterDevAPI/issues/65/
        # default_value can use special characters: https://admin.zapier.com/rover/app/ZapierFormatterDevAPI/issues/54/
        if not isinstance(inputs, list):
            return self.get_defaulted_value(inputs, options['default_value'])
        elif not inputs:
            # we were provided a line-item field, give them one back
            return [expand_special_chargroups(options['default_value'])]
        else:
            output = []
            for input in inputs:
                output.append(self.get_defaulted_value(input, options['default_value']))
            return output


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



register(StringDefaultValueV2Transform())
