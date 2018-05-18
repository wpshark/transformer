from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number, expand_special_chargroups

import random


class UtilFlattenLineItem(BaseTransform):

    category = 'util'
    name = 'flatten'
    label = 'Flatten line-item'
    help_text = 'Take an array/line-item as input and output as a string.'

    noun = 'Line-item'
    verb = 'Flatten'

    def transform_many(self, str_input, separator=u'', **kwargs):
        """
        Override the standard behavior of the transform_many by only
        accepting list inputs which we use to perform the choose operation.

        """
        if not inputs:
            return u''

        if not isinstance(inputs, list):
            self.raise_exception('Flatten requires a line-item as input')

        separator = expand_special_chargroups(separator)

        if separator:
            segments = separator.join(str_input)
        else:
            segments = ','.join(str_input)

        return segments


    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
                'key': 'separator',
                'label': 'Separator',
                'help_text': 'Character to seperate flattened line-item with. (Default: `,`) For supported special characters, see: https://zapier.com/help/formatter/#special-characters)' # NOQA
            },
        ]


    def truthy_inputs(self, inputs):
        """ return only truthy inputs """
        return [v for v in inputs if (not isinstance(v, basestring) and v is not None) or v]


    def choose_first(self, inputs, default=None):
        """
        choose the first _truthy_ string value or the first non-string value
        or the default value if there is neither.

        """
        return self.choose_nth(0, inputs, default=default)


    def choose_last(self, inputs, default=None):
        """
        choose the last _truthy_ string value or the last non-string value
        or the default value if there is none.

        """
        return self.choose_nth(-1, inputs, default=default)


    def choose_nth(self, n, inputs, default=None):
        """
        choose the n-th _truthy_ string value or the n-th non-string value
        or the default value if there is neither.

        """
        try:
            return self.truthy_inputs(inputs)[n]
        except:
            pass
        return default


    def choose_random(self, inputs, default=None):
        """
        choose a random _truthy_ string value or a random non-string value
        or the default value if there is neither.

        """
        truthy = self.truthy_inputs(inputs)
        if not truthy:
            return default
        return random.choice(truthy)


register(UtilFlattenLineItem())
