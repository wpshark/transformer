from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import expand_special_chargroups


class UtilLineItemToStringV2Transform(BaseTransform):

    category = 'util'
    name = 'lineitem_to_string_v2'
    label = 'Line-item to Text'
    help_text = (
        'Convert a line-item to delimited text. [a,b,c,d] becomes \'a,b,c,d\'. Also returns '
        ' each element of the line-item as a separate field. More on line-items '
        '[here](https://zapier.com/help/formatter/#how-use-line-items-formatter).'
    )

    noun = 'Line-Item'
    verb = 'Convert'

    def transform_many(self, inputs, options=None, **kwargs):
        """
        Override the standard behavior of the transform_many by only
        accepting list inputs which we use to perform the choose operation.

        """
        
        output = {}
        
        #Perform main function of Line item to string:

        if not inputs:
            output["text_output"] = ''
            return output

        #update for Loki issue, return string is only one element
        if not isinstance(inputs, list):
            output["text_output"] = inputs
            output["item 1"] = inputs
            return output

        if options is None:
            options = {}

        separator = expand_special_chargroups(options.get('separator'))

        if separator:
            text_ouput = separator.join(inputs)
        else:
            text_ouput = ','.join(inputs)

        output["text_output"] = text_ouput

        #Create Separate Fields
        
        for i, v in enumerate(inputs):
            output["item "+str(i+1)] = v
            
        return output


    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
                'key': 'separator',
                'label': 'Separator',
                'help_text': (
                    'Character(s) to delimit text with. (Default: \',\') '
                    'For supported special characters, see: https://zapier.com/help/formatter/#special-characters)'
                ),  # NOQA
            },
        ]


register(UtilLineItemToStringV2Transform())
