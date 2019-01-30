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
        filtered_table = {}
        separate_lists = {}
        longest_array = 0

        #filter out entries with no key
        for k, v in table.iteritems():
            if not k == u'':
                filtered_table.update({k:v})

        
        #split each string value in the dict by ',' and determine the 
        #  length oflongest array
        for k, v in filtered_table.iteritems():
            separate_lists[k] = v.split(',')
            if len(separate_lists[k]) > longest_array:
                longest_array = len(separate_lists[k])

        #make mini objects to add to the output object
        for num in range(0,longest_array):
            this_line_item = {}
            for i, (k, v) in enumerate(filtered_table.items()):
                try:
                    this_line_item.update({k: separate_lists[k][num]})
                except: 
                    n = 0
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
                    'text and converted back to a line-item along with any other text you add. This can be used '
                    'to append or prepend values to existing line items.'
            }
        ]


register(UtilStringToLineItemsTransform())
