from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number, expand_special_chargroups

import random


class UtilFlattenTransform(BaseTransform):

    category = 'util'
    name = 'flatten'
    label = 'Flatten line-item'
    help_text = 'Take a line-item as input and output a seperated string. [a,b,c,d] becomes `a,b,c,d`'

    noun = 'Line-item'
    verb = 'Flatten'

    def transform_many(self, inputs, options=None, **kwargs):
        """
        Override the standard behavior of the transform_many by only
        accepting list inputs which we use to perform the choose operation.

        """
        
        if not inputs:
            return u''
        
        if not isinstance(inputs, list):
            self.raise_exception('Flatten requires a line-item as input')
        
        # make sure if there any empty elements are replace with ''
        inputs = [(x if x is not None else '') for x in inputs]
        
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
                'help_text': 'Character to seperate flattened line-item with. (Default: `,`) For supported special characters, see: https://zapier.com/help/formatter/#special-characters)' # NOQA
            },
        ]


register(UtilFlattenTransform())
