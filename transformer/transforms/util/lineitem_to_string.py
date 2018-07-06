from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number, expand_special_chargroups

import random


class UtilLineItemToStringTransform(BaseTransform):

    category = 'util'
    name = 'lineitem_to_string'
    label = 'Convert Line-Item to Text'
    help_text = 'Convert a line-item to delimited text. [a,b,c,d] becomes `a,b,c,d`'

    noun = 'Line-Item'
    verb = 'Convert'

    def transform_many(self, inputs, options=None, **kwargs):
        """
        Override the standard behavior of the transform_many by only
        accepting list inputs which we use to perform the choose operation.

        """
        
        if not inputs:
            return u''
        
        if not isinstance(inputs, list):
            self.raise_exception('Convert requires a line-item as input')
        
        if options is None:
            options = {}
        
        separator = expand_special_chargroups(options.get('separator'))

        if separator:
            segments = separator.join(inputs)
        else:
            segments = ','.join(inputs)

        return segments


    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
                'key': 'separator',
                'label': 'Separator',
                'help_text': 'Character(s) to delimit line-item with. (Default: `,`) For supported special characters, see: https://zapier.com/help/formatter/#special-characters)' # NOQA
            },
        ]


register(UtilLineItemToStringTransform())
