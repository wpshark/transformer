import operator

from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number


class NumberMathTransform(BaseTransform):

    category = 'number'
    name = 'math'
    label = 'Perform Math Operation'
    help_text = 'Perform mathematical operations on value(s)'

    _operations = {
        'add': (2, operator.add),
        'sub': (2, operator.sub),
        'mul': (2, operator.mul),
        'div': (2, lambda a, b: operator.div(float(a), b)),
        'neg': (1, operator.neg)
    }

    def transform_many(self, inputs, options=None, **kwargs):
        """
        Override the standard behavior of the transform_many by only
        accepting list inputs which we use to perform math operations.

        """
        if not isinstance(inputs, list):
            self.raise_exception('Math Operations require a list of inputs')

        if options is None:
            options = {}

        # try converting inputs to numbers
        inputs = map(try_parse_number, inputs)

        # get the operation
        op = options.get('operation')
        if not op or op not in self._operations:
            self.raise_exception('Invalid Operation')

        operands, op_func = self._operations.get(op)

        # unary operations return a list
        if operands == 1:
            return map(op_func, inputs)

        # binary operations return an accumulated value
        initial, rest = inputs[0], inputs[1:]
        value = reduce(op_func, rest, initial)
        return value


    def all_fields(self, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'operation',
                'choices': 'add|Add,sub|Subtract,mul|Multiply,div|Divide,neg|Make Negative',
                'help_text': 'The math operation to perform.'
            },
            self.build_list_input_field()
        ]

register(NumberMathTransform())
