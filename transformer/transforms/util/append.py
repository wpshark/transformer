from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number, expand_special_chargroups

import random


class UtilAppendTransform(BaseTransform):

    category = 'util'
    name = 'append'
    label = 'Append to line-item'
    help_text = 'Append a text element to a line-item. e appended to [a,b,c,d] becomes [a,b,c,d,e]'

    noun = 'Line-item'
    verb = 'Append'

    def transform_many(self, inputs, options=None, **kwargs):
        """
        Override the standard behavior of the transform_many by only
        accepting list inputs which we use to perform the choose operation.

        """
        
        if options is None:
            return inputs
        
        append_text = expand_special_chargroups(options.get('append_text'))
                
        if not isinstance(inputs, list):
            self.raise_exception('Append requires a line-item as input')
        
        new_inputs = [(x if x is not None else '') for x in inputs]
        # hacky way if we have one element, but it's nothing, might as well return the append string
        if (len(new_inputs) == 1 and new_inputs[0] == '') :
            return [append_text]
        
        new_inputs.append(append_text)
        return new_inputs


    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
                'key': 'append_text',
                'label': 'Text to append',
                'help_text': 'Text element that you wish to append to the end of the line-item.' # NOQA
            },
        ]




register(UtilAppendTransform())
