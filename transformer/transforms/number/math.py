from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.util import try_parse_number

import inspect
import operator

class NumberMathTransform(BaseTransform):

    category = 'number'
    name = 'math'
    label = 'Number / Math'
    help_text = 'Perform mathematical operations on value(s)'

    _operations = {
        'sum': (2, operator.add),
        'sub': (2, operator.sub),
        'mul': (2, operator.mul),
        'div': (2, lambda a, b: operator.div(float(a), b)),
        'neg': (1, operator.neg)
    }


    def transform_many(self, inputs, data=None, **kwargs):
        """
        we override the standard behavior of the transform_many by only
        accepting list inputs which we use to perform math operations.

        """
        if not isinstance(inputs, list):
            self.raise_exception('Math Operations Require a List of Inputs')

        if data is None:
            data = {}

        # try converting inputs to numbers
        inputs = map(try_parse_number, inputs)

        # get the operation
        op = data.get('operation')
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


    def fields(self, **kwargs):
        return [
            {
                'type': 'unicode',
                'required': True,
                'key': 'operation',
                'choices': 'sum|Sum,sub|Subtract,mul|Multiply,div|Divide,neg|Make Negative',
                'help_text': 'What type of math would you like to do?'
            },
            {
                'type': 'unicode',
                'list': True,
                'required': True,
                'key': 'inputs',
                'help_text': 'Value(s) you would like to transform'
            }
        ]

register(NumberMathTransform())
