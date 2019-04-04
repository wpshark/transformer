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

    def transform(
        self,
        input_key,
        my_dict={},
        my_price="Price",
        my_qty="Quantity",
        my_subtotal_name="Subtotal",
        my_decimals="2",
        my_subtotal_toggle="No",
        my_numbering_name="Number",
        my_numbering_toggle="No",
        **kwargs
    ):
        """Take a dict input and output an array of one or more Zapier standard line-items.
        Subtotal value takes the values from two other fields like Price and Quantity and multiplies them
        Number value starts at 1 and increments by 1 for each line item, providign an accessible line item number for users

        Example:
        User inputs some strings and a dict like this:
            input_key = "Order Lines"
            my_dict = { 
                "Price": "5,3.5,4",
                "Description": "Hat,Shoes,Shirt",
                "Quantity": "1,2,1"
            }
            my_price = "Price"
            my_qty = "Quantity"
            my_subtotal_name = "Subtotal"
            my_decimals = "2"
            my_subtotal_toggle = "Yes"
            my_numbering_name="Number",
            my_numbering_toggle="Yes",
        Expected output (Zapier Standard Line Items with optional, calculated Subtotal property):
            {
                Order Lines": [
                    {
                        "Price": "5",
                        "Description": "Hat",
                        "Quantity": "1",
                        "Subtotal": "5",
                        "Number": "1"
                    },
                    {
                        "Price": "3.5",
                        "Description": "Shoes",
                        "Quantity": "2",
                        "Subtotal": "7",
                        "Number": "2"
                    },
                    {
                        "Price": "4",
                        "Description": "Shirt",
                        "Quantity": "1",
                        "Subtotal": "4",
                        "Number": "3"
                    }
                ]
            }
        """

        # make sure that a name is set for the line-item group
        if not input_key:
            input_key = "Line-item(s)"

        # initialize output and other variables
        output = {input_key: []}
        numbering_increment = 1
        longest_array = 0
        price = Decimal(0)
        qty = Decimal(0)
        my_decimals = try_parse_number(my_decimals)
        try:
            my_places = Decimal(10) ** (-1 * int(my_decimals))
        except ValueError as e:
            self.raise_exception(
                "Please enter an integer for the 'Decimal Places for Subtotal Values' field."
            )

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
            if (
                my_price in this_line_item.keys()
                and my_qty in this_line_item.keys()
                and my_subtotal_toggle == "Yes"
                and my_subtotal_name not in my_dict.keys()
            ):
                # Try to create a subtotal value for this line item if:
                #   Create Subtotal Property is "Yes"
                #   There is no conflict between a Line-item property with the same name as the Subtotal field
                #   The Specified Price and Quantity fields exist in this line item.
                try:
                    price = Decimal(this_line_item[my_price])
                    qty = Decimal(this_line_item[my_qty])
                    this_line_item.update(
                        {my_subtotal_name: str((price * qty).quantize(my_places))}
                    )
                except (KeyError, ValueError, InvalidOperation) as e:
                    # These are the three error types we'd expect to happen in this block, although KeyError is minimized
                    # by the if statement
                    pass
            if my_numbering_toggle == "Yes" and my_numbering_name not in my_dict.keys():
                # Create a number value that users can access in their Zaps:
                try:
                    this_line_item.update({my_numbering_name: str(numbering_increment)})
                except ValueError as e:
                    pass
            # try adding the individual line item object to the main output array. Skips if no object is available (unlikely).
            try:
                output[input_key].append(this_line_item)
                numbering_increment += 1
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
                "help_text": "If you have 'Price' and 'Quantity' properties in your line items, Line Itemizer "
                "can multiply those values together to create a corresponding 'Subtotal' property. "
                "If they're called something else, you can specify which two properties to multiply below. "
                "[Learn more about the Subtotal property here](https://zapier.com/help/formatter/#create-your-own-line-items-for-an-invoicing-action-using-the-line-itemizer-utility).",
            },
            {
                "type": "unicode",
                "required": False,
                "key": "my_subtotal_toggle",
                "label": "Create Subtotal Property?",
                "default": "No",
                "choices": "Yes,No",
            },
            {
                "type": "unicode",
                "required": False,
                "key": "my_price",
                "label": "Price Property to use for calculating Subtotal",
                "default": "Price",
            },
            {
                "type": "unicode",
                "required": False,
                "key": "my_qty",
                "label": "Quantity Property to use for calculating Subtotal",
                "default": "Quantity",
            },
            {
                "type": "unicode",
                "required": False,
                "key": "my_subtotal_name",
                "label": "Subtotal Property Name",
                "default": "Subtotal",
                "help_text": "Set the Subtotal Property Name here. Default is 'Subtotal'. Formatter will not "
                "overwrite a property with the same name defined in the 'Line-item Properties' fields.",
            },
            {
                "type": "int",
                "required": False,
                "key": "my_decimals",
                "label": "Decimal Places for Subtotal Values",
                "default": "2",
                "help_text": "Specify how many decimal places each Subtotal value should be rounded to. "
                "Default is '2'.",
            },
            {
                "key": "numbering_help",
                "type": "copy",
                "help_text": "If you want to number your line-items, Formatter can create a 'Number' property "
                "in each line-item. Starts at 1 and increments by 1 for each line. ",
            },
            {
                "type": "unicode",
                "required": False,
                "key": "my_numbering_toggle",
                "label": "Create Number Property?",
                "default": "No",
                "choices": "Yes,No",
            },
            {
                "type": "unicode",
                "required": False,
                "key": "my_numbering_name",
                "label": "Number Property Name",
                "default": "Number",
                "help_text": "Set the Number Property Name here. Default is 'Number'. Formatter will not "
                "overwrite a property with the same name defined in the 'Line-item Properties' fields.",
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
