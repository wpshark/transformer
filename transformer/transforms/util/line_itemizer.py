from transformer.registry import register
from transformer.transforms.base import BaseTransform


class UtilLineItemizerTransform(BaseTransform):

    category = "util"
    name = "line_itemizer"
    label = "Line Itemizer (Create/Append/Prepend)"
    # Flesh this out to describe more functions
    help_text = (
        "Convert comma delimited text or values to line-item(s). 'a,b,c,d' becomes [a,b,c,d]. Append "
        "or prepend to existing line-items by mapping them into the same field as comma separated "
        "text or single values. For details, learn more about "
        "[Line-items with Formatter](https://zapier.com/help/formatter/#how-use-line-items-formatterv2), "
        "or jump to [Line Itemizer examples](https://zapier.com/help/formatter/#create-your-own-line-items-for-an-invoicing-action-using-the-line-itemizer-utility)."
    )

    noun = "Text"
    verb = "convert"
    lineitems_group_name_error = (
        "The 'Line-item(s) Group Name' field should only contain text or single values"
    )

    def build_input_field(self):
        return {
            "type": "unicode",
            "required": False,
            "key": "inputs",
            "label": "Line-item(s) Group Name",
            "help_text": "Name your set of line-item(s). ex: 'Orders', 'Invoice Lines'. Default is 'Line-item(s)'.",
        }

    def transform(self, input_key, my_dict={}, **kwargs):
        """Take a dict input and output an array of one or more Zapier standard line-items.

        Example:
        User inputs a string and a dict like this:
            input_key = "Order Lines"
            my_dict = { 
                "Price": "5,3.5,4",
                "Description": "Hat,Shoes,Shirt",
                "Quantity": "1,2,1"
            }
        Expected output:
            {
                Order Lines": [
                    {
                        "Price": "5",
                        "Description": "Hat",
                        "Quantity": "1"
                    },
                    {
                        "Price": "3.5",
                        "Description": "Shoes",
                        "Quantity": "2"
                    },
                    {
                        "Price": "4",
                        "Description": "Shirt",
                        "Quantity": "1"
                    }
                ]
            }
        """

        # make sure that a name is set for the line-item group
        if not input_key:
            input_key = "Line-item(s)"

        # initialize output and other variables
        output = {input_key: []}
        longest_array = 0

        # filter out entries with no key
        my_dict.pop("", None)

        # split each string value in the dict by ',' and determine the
        #  length of longest array
        for k, v in my_dict.items():  # might not need iteritems
            my_dict[k] = v.split(",")
            if len(my_dict[k]) > longest_array:
                longest_array = len(my_dict[k])

        # make individual objects for each line (example: could include 1 value each of qty, description, price) to add to the output object
        for num in range(0, longest_array):
            # initialize a new individual line-item
            this_line_item = {}
            for k, v in my_dict.items():
                # Try to add each property from my_dict to the individual line-item.
                #  Skips if the list isn't long enough for an available property.
                try:
                    this_line_item.update({k: v[num]})
                except IndexError as e:
                    pass
            # try adding the individual line item object to the main output array. Skips if no object is available (unlikely).
            try:
                output[input_key].append(this_line_item)
            except IndexError as e:
                pass

        return output

    def fields(self, *args, **kwargs):
        return [
            {
                "type": "dict",
                "required": False,
                "key": "my_dict",
                "label": "Line-item(s)",
                "help_text": "Line-item property names on the left (ex: Price, Description) and comma-separated "
                "text or values on the right.",
            }
        ]

    def transform_many(self, inputs, options):
        """
        Throws error if lists or dicts are mapped into the 'Line-item(s) Group Name'/'inputs' field.
        """

        options = options or {}

        if isinstance(inputs, (dict, list)):
            self.raise_exception("{}".format(self.lineitems_group_name_error))
        else:
            outputs = self.transform(inputs, **options)
        return outputs


register(UtilLineItemizerTransform())
