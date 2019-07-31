from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number
import json


class UtilFixLineitemsTransform(BaseTransform):

    category = "util"
    name = "fix_lineitems"
    label = "Fix malformed line-item field(s)"

    noun = "Line-item"
    verb = "fix"
    help_text = 'If you have line-item fields with [ ] in the field text, they are likely malformed. This utility will attempt to reconstruct these field(s).'

    def build_input_field(self):
        # this is a hack, but having inoput being declared as a dict hides it
        # rather than do one more hack to the Formatter scripting code
        return [
            {
                'type': 'dict',
                'required': False,
                'key': 'inputs',
                'label': 'Line-item Fields',
            }
        ]
        
    def transform(self, inputs, my_dict=None, **kwargs):
        """Take a dict input and output each object as an array (line-itme field)
        
        """
        # make individual objects for each line 
        # initialize a new individual line-item
        this_line_item = {}
        for k, v in my_dict.items():
            # First check if it is a list, then just return the value
            # If not, then split the string to create our new array
            if isinstance(my_dict, list):
                this_line_item[k] = v
            else:
                this_line_item[k] = v.split(',')
        return this_line_item

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'dict',
                'required': False,
                'key': 'my_dict',
                'label': 'Line-item Fields',
                'help_text': ( 
                    'New Line-item field names on the left and your '
                    'mapped malformed line-item fields on the right.'
                ),  # NOQA
            }
        ]
        
register(UtilFixLineitemsTransform())