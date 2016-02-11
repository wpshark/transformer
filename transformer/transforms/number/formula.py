from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.transforms.number.formula_tokenizer import shunting_yard, FunctionNode, OperatorNode, OperandNode, RangeNode
from transformer.util import math, int_or_float

import collections
import operator

Func = collections.namedtuple('Func', ['n', 'f'])

def evaluate(formula):
    """ evaluate an excel-style formula """
    functions = {
        'MAX':     Func(0, wrap_reduce(max)),
        'MIN':     Func(0, wrap_reduce(min)),
        'MOD':     Func(2, operator.mod),
        'SQRT':    Func(1, math.sqrt),
        'POW':     Func(2, math.pow),
        'CEILING': Func(-1, math.ceil),
        'FLOOR':   Func(-1, math.floor),
        'ROUND':   Func(-1, round),
        'IF':      Func(-2, op_if),
        'AND':     Func(-1, wrap_varlist(all)),
        'OR':      Func(-1, wrap_varlist(any)),
    }

    operators = {
        'u-': Func(1, operator.neg),             # unary negation
        'u%': Func(1, lambda a: a / float(100)), # unary percentage
        '+':  Func(2, operator.add),
        '-':  Func(2, operator.sub),
        '/':  Func(2, operator.truediv),
        '*':  Func(2, operator.mul),
        '=':  Func(2, operator.eq),
        '<>': Func(2, lambda a, b: not operator.eq(a, b)),
        '>':  Func(2, operator.gt),
        '<':  Func(2, operator.lt),
        '>=': Func(2, operator.ge),
        '<=': Func(2, operator.le),
    }

    # first, parse the formula into reverse polish notation
    rpn = parse_rpn(formula)

    # check the nodes to make sure they are valid
    for i, n in enumerate(rpn):
        key = str(n).upper()
        if isinstance(n, RangeNode):
            if n.token.tsubtype not in ('logical', 'text'):
                raise Exception('Invalid Syntax: Only numeric values are allowed.')
        if isinstance(n, FunctionNode) and key not in functions:
            raise Exception('Unknown Function: {}'.format(n))
        if isinstance(n, OperatorNode) and key not in operators and 'u{}'.format(key) not in operators:
            raise Exception('Unknown Operation: {}'.format(n))

    # evaluate the reverse polish notation
    stack = []
    for n in rpn:
        if isinstance(n, OperandNode):
            stack.append(eval_operand(n))

        if isinstance(n, FunctionNode):
            num = n.num_args
            func = functions.get(str(n).upper())
            if func.n < 0 and num < -func.n:
                raise Exception('Invalid Formula: {} requires at least {} arguments'.format(str(n), -func.n))
            if func.n > 0 and num != func.n:
                raise Exception('Invalid Formula: {} requires {} arguments ({} supplied)'.format(str(n), func.n, num))
            stack, args = stack[:-num], stack[-num:]
            stack.append(func.f(*args))

        if isinstance(n, OperatorNode):
            num = 2 if n.token.ttype.endswith('infix') else 1
            key = str(n).upper()
            if num == 1:
                key = 'u{}'.format(key)
            op = operators.get(key)
            if op.n < 0 and num < -op.n:
                raise Exception('Invalid Formula: {} requires at least {} arguments'.format(str(n), -op.n))
            if op.n > 0 and num != op.n:
                raise Exception('Invalid Formula: {} requires {} arguments ({} supplied)'.format(str(n), op.n, num))
            stack, args = stack[:-num], stack[-num:]
            stack.append(op.f(*args))

    # if there's any stack left...the formula is invalid
    # all formulas should reduce to a single value
    if len(stack) > 1:
        raise Exception('Invalid Formula.')

    return stack.pop()

def parse_rpn(formula):
    """ parse a formula into reverse polish notation """
    return shunting_yard(formula)

def eval_operand(n):
    """ evaluate an operand into a numeric value """
    if not isinstance(n, OperandNode):
        return None
    if n.token.tsubtype == 'number':
        return int_or_float(float(n.token.tvalue))
    if n.token.tsubtype == 'logical':
        return 1 if 'TRUE' in n.token.tvalue else 0
    # if we want to use allow text output, this will be needed
    # if n.token.tsubtype == 'text':
    #     return n.token.tvalue
    raise Exception('Invalid Operand: Only numeric values allowed. ({} provided)'.format(n.token.tsubtype))

def wrap_reduce(f):
    """ wrap a 2 argument function as a multi-argument function via reduce """
    def _wrap(*args):
        if len(args) <= 2:
            return f(*args)
        return reduce(f, args)
    return _wrap

def wrap_varlist(f):
    """ wrap a 1 argument function as a multi-argument function via list """
    def _wrap(*args):
        return f(args)
    return _wrap

def op_if(test, true_value, *args):
    """ operator for if functions """
    false_value = args[0] if args else None
    return true_value if test else false_value

class NumberFormulaTransform(BaseTransform):
    category = 'number'
    name = 'formula'
    label = 'Number Formula'
    help_text = 'Transform a number with an Excel-style formula.'

    def transform(self, formula):
        return evaluate(formula)

    def all_fields(self, *args, **kwargs):
        input_field = self.build_input_field()
        input_field['label'] = 'Formula'
        input_field['help_text'] = 'Excel-style formula to evaluate'
        return [input_field]

register(NumberFormulaTransform())
