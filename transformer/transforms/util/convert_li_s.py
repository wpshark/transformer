from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number, expand_special_chargroups

import random


class UtilConvertLineItemToStringTransform(BaseTransform):

    category = 'util'
    name = 'convert_li_s'
    label = 'Convert line-item'
    help_text = 'Convert a line-item to a delimited string. [a,b,c,d] becomes `a,b,c,d`'

    noun = 'Line-item'
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
        
        # Do I need to check for empty list/array elements?
        new_inputs = [(x if x is not None else '') for x in inputs]
        
        separator = expand_special_chargroups(options.get('separator'))

        if separator:
            segments = separator.join(new_inputs)
        else:
            segments = ','.join(new_inputs)

        return segments


    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
                'key': 'separator',
                'label': 'Separator',
                'help_text': 'Character to delimit line-item with. (Default: `,`) For supported special characters, see: https://zapier.com/help/formatter/#special-characters)' # NOQA
            },
        ]


register(UtilConvertLineItemToStringTransform())
