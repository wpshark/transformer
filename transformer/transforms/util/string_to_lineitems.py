from transformer.registry import register
from transformer.transforms.base import BaseTransform


class UtilStringToLineItemsTransform(BaseTransform):

    category = 'util'
    name = 'string_to_lineitems'
    label = 'Text to Line-item(s)'
    help_text = (
        'Convert comma delimited text to line-item(s). \'a,b,c,d\' becomes [a,b,c,d]. More on line-items '
        '[here](https://zapier.com/help/formatter/#how-use-line-items-formatter).'
    )
    
    noun = 'Text'
    verb = 'convert'

    def build_input_field(self):
        return {
            'type': 'unicode',
            'required': False,
            'key': 'inputs',
            'label': 'Line-item(s) Group Name',
            'help_text': 'Optional name for your set of line-item(s). ex: "Orders", "Sale lines", etc. Default is "Line-item(s)".'
        }

    def transform(self, input_key, table={}, **kwargs):
        
        #make sure that a name is set for the line-item group
        if not input_key:
            input_key = u'Line-item(s)'

        #initialize output and separate lists dicts
        output = {input_key: []}
        separate_lists = {}
        longest_array = 0

        #filter out entries with no key
        table.pop('', None)

        #split each string value in the dict by ',' and determine the 
        #  length oflongest array
        for k, v in table.iteritems():
            separate_lists[k] = v.split(',')
            if len(separate_lists[k]) > longest_array:
                longest_array = len(separate_lists[k])

        #make mini objects to add to the output object
        for num in range(0,longest_array):
            #initialize single line item
            this_line_item = {}
            for i, (k, v) in enumerate(table.items()):
                #try to add each property from the Dict / table to the single line item. Skips if no property is available.
                try:
                    this_line_item.update({k: separate_lists[k][num]})
                except: 
                    n = 0 
            #try adding single line item object to the main output array
            try:
                output[input_key].append(this_line_item)
            except:
                n = 0
            
        return output

    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'dict',
                'required': False,
                'key': 'table',
                'label': 'Line-item(s)',
                'help_text': 'Line-item property names on the left (ex: Price, Description) and comma-separated '
                    'values on the right. Each property must have a unique name. Properties without a name are '
                    'ignored. Line-items mapped into the fields on the right will be treated as comma-separated '
                    'text along with any plain text or single values you add. This can be used to append or '
                    'prepend values to existing line-items.'
            }
        ]


register(UtilStringToLineItemsTransform())
