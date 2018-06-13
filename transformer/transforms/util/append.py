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
        
        #append_txt could be a list/array, so lets clean it up, and if it's not one, make it so we just use the concatenate command later
        append_text = options.get('append_text')
        if isinstance(append_text, list):
            append_text = [(x if x is not None else '') for x in append_text]
        else:
            append_text = [append_text]

        #new_inputs = inputs
        #inputs is a list/array, so lets clean it up before we do the append
        new_inputs = [(v if v is not None else '') for v in inputs]
        # hacky way if we have one element, but it's nothing, might as well return the append string
        if (len(new_inputs) == 1 and new_inputs[0] == '') :
            return append_text
        else:
            return (new_inputs + append_text)
        


    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
                'key': 'append_text',
                'label': 'Text to append',
                'help_text': 'Text that you wish to append to the end of the line-item.' # NOQA
            },
        ]




register(UtilAppendTransform())
