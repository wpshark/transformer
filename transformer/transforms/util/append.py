from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number, expand_special_chargroups

import random


class UtilAppendTransform(BaseTransform):

    category = 'util'
    name = 'append'
    label = 'Append to line-item'
    help_text = 'e appended to [a,b,c,d] becomes [a,b,c,d,e]'

    noun = 'Line-item'
    verb = 'Append'

    def transform_many(self, inputs, options=None, **kwargs):
        """
        Override the standard behavior of the transform_many by only
        accepting list inputs which we use to perform the choose operation.

        """
        
        if options is None:
            return inputs
        
        if not isinstance(inputs, list):
            self.raise_exception('Append requires a line-item as input')
        
        #append_text input could be a list/array, if it's not one, make it so we just use the concatenate command later
        if isinstance(options.get('append_text'), list):
            append_text = options.get('append_text')
        else:
            append_text = [options.get('append_text')]

        # Do I need to check for empty list/array elements, lets not today and see how it goes with initial release?
        # new_inputs = [(v if v is not None else '') for v in inputs]
        
        # hacky way if we have one element, but it's nothing, might as well return the append string
        if (len(inputs) == 1 and inputs[0] == '') :
            return append_text
        else:
            return (inputs + append_text)
        


    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
                'key': 'append_text',
                'label': 'Text to append',
                'help_text': 'Text (can be a string or a line-item) that you wish to add to the end of the line-item field.' # NOQA
            },
        ]




register(UtilAppendTransform())
