from transformer.registry import register
from transformer.transforms.base import BaseTransform

class UtilAppendTransform(BaseTransform):

    category = 'util'
    name = 'append'
    label = 'Append to Line-Item'
    help_text = '\'e\' appended to [a,b,c,d] becomes [a,b,c,d,e]. More on line-items [here.](https://zapier.com/help/formatter/#how-use-line-items-formatter)'

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

        append_text_input = options.get('append_text')
        is_list = isinstance(append_text_input, list)
        append_text = append_text_input if is_list else append_text_input.split(',')
        # used to be [append_text_input], changing to a split here to see if we can get the values

        # hacky way if we have one element, but it's nothing, might as well return the append string
        if len(inputs) == 1 and not inputs[0]:
            return append_text

        return inputs + append_text


    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': False,
                'key': 'append_text',
                'label': 'Text to append',
                'help_text': 'Text that you wish to add to the end of the line-item field. Also supports line-items.' # NOQA
            },
        ]




register(UtilAppendTransform())
