from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number
from decimal import *


class UtilLineItemizerTransform(BaseTransform):

    category = "util"
    name = "line_itemizer"
    label = "Line Itemizer (Create/Append/Prepend)"
    # Flesh this out to describe more functions
    help_text = (
        "Convert comma delimited text or values to line-item(s). 'a,b,c,d' becomes [a,b,c,d]. Append "
        "or prepend to existing line-items by mapping them into the same field as comma separated "
        "text or single values. For details, learn more about "
        "[Line-items with Formatter](https://zapier.com/help/create/format/create-line-items-in-zaps)."
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

    def transform(
        self, input_key, my_dict=None, decimals=2, subtotal_toggle=False, **kwargs
    ):
        """Take a dict input and output an array of one or more Zapier standard line-items.
        Subtotal value takes the values from two other fields like Price and Quantity and multiplies them

        Example:
        User inputs some strings and a dict like this:
            input_key = "Order Lines"
            my_dict = { 
                "Price": "5,3.5,4",
                "Description": "Hat,Shoes,Shirt",
                "Quantity": "1,2,1"
            }
            decimals = "2"
            subtotal_toggle=True,
        Expected output (Zapier Standard Line Items with optional, calculated Subtotal property):
            {
                Order Lines": [
                    {
                        "Price": "5",
                        "Description": "Hat",
                        "Quantity": "1",
                        "Subtotal": "5.00"
                    },
                    {
                        "Price": "3.5",
                        "Description": "Shoes",
                        "Quantity": "2",
                        "Subtotal": "7.00
                    },
                    {
                        "Price": "4",
                        "Description": "Shirt",
                        "Quantity": "1",
                        "Subtotal": "4.00"
                    }
                ]
            }
        """

        # make sure that a name is set for the line-item group
        if not input_key:
            input_key = "Line-item(s)"

        # initialize variables
        if my_dict is None:
            my_dict = {}
        output = {input_key: []}
        longest_array = 0
        subtotal = "subtotal"
        price = "Price"
        qty = "Quantity"

        # check for alternative cases for property names for price and quantity
        if price not in my_dict:
            for k in my_dict:
                if k.lower() == "price":
                    price = k
        if qty not in my_dict:
            for k in my_dict:
                if k.lower() == "quantity":
                    qty = k
                elif k.lower() == "qty":
                    qty = k

        decimals = try_parse_number(decimals)
        try:
            my_places = Decimal(10) ** (-1 * int(decimals))
        except ValueError as e:
            self.raise_exception(
                "Please enter an integer for the 'Decimal Places for Subtotal Values' field."
            )

        # filter out entries with no key
        my_dict.pop("", None)

        # split each string value in the dict by ',' and determine the
        #  length of longest array
        for k, v in list(my_dict.items()):  # might not need iteritems
            my_dict[k] = v.split(",")
            if len(my_dict[k]) > longest_array:
                longest_array = len(my_dict[k])

        # make individual objects for each line (example: could include 1 value each of qty, description, price) to add to the output object
        for num in range(0, longest_array):
            # initialize a new individual line-item
            this_line_item = {}
            for k, v in list(my_dict.items()):
                # Try to add each property from my_dict to the individual line-item.
                #  Skips if the list isn't long enough for an available property.
                try:
                    this_line_item[k] = v[num]
                except IndexError as e:
                    pass
            if price in this_line_item and qty in this_line_item and subtotal_toggle:
                # Try to create a subtotal value for this line item if:
                #   Create Subtotal Property is "Yes"
                #   There is no conflict between a Line-item property with the same name as the Subtotal field
                #   The Price and Quantity fields both exist in this line item.
                try:
                    decimal_price = Decimal(this_line_item[price])
                    decimal_qty = Decimal(this_line_item[qty])
                    # must convert to string or float here, or else output will include the text "Decimal()"
                    this_line_item[subtotal] = str(
                        (decimal_price * decimal_qty).quantize(my_places)
                    )
                except (KeyError, ValueError, InvalidOperation) as e:
                    # These are the three error types we'd expect to happen in this block, although KeyError is minimized
                    # by the if statement
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
                "label": "Line-item Properties",
                "help_text": "Line-item property names on the left (ex: Price, Description) and comma-separated "
                "text or values on the right.",
            },
            {
                "key": "subtotal_help",
                "type": "copy",
                "help_text": "If you have properties called 'Price' and 'Quantity' (or 'Qty') in your line-items above, "
                "Line Itemizer can multiply those values together to create a corresponding 'Subtotal' property. "
                "[Learn more about the Subtotal property here](https://zapier.com/help/doc/how-use-line-items-formatterv2#create-line-items-with-subtotals-using-the-line-itemizer-utility).",
            },
            {
                "type": "bool",
                "required": False,
                "key": "subtotal_toggle",
                "label": "Create Subtotal Property?",
                "default": "no",
            },
            {
                "type": "int",
                "required": False,
                "key": "decimals",
                "label": "Decimal Places for Subtotal Values",
                "default": "2",
            },
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
