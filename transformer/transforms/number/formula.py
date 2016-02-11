from transformer.registry import register
from transformer.transforms.base import BaseTransform
from transformer.transforms.number.formula_tokenizer import shunting_yard, FunctionNode, OperatorNode, OperandNode, RangeNode
from transformer.util import math, int_or_float

import collections
import fractions
import operator
import random


def get_default_functions():
    """
    generate a mapping of default functions allowed for evaluation

    reference: http://www.excelfunctions.net/ExcelFunctions.html
    """
    return {
        'MAX': Func(0, wrap_reduce(max)),
        'MIN': Func(0, wrap_reduce(min)),

        # Basic Numeric Information
        'ABS': Func(1, operator.abs),
        'SIGN': Func(1, func_sign),
        'GCD': Func(-2, wrap_reduce(fractions.gcd)),
        'LCM': Func(-2, wrap_reduce(func_lcm)),

        # Basic Math Operations
        'SUM': Func(-2, wrap_reduce(operator.add)),
        'PRODUCT': Func(-2, wrap_reduce(operator.mul)),
        'SQRT': Func(1, math.sqrt),
        'POWER': Func(2, math.pow),
        'QUOTIENT': Func(2, operator.div),
        'MOD': Func(2, operator.mod),

        # Basic Rounding Functions
        'CEILING': Func(-1, func_ceil), # ceiling with factor
        'FLOOR': Func(-1, func_floor),  # floor with factor
        'EVEN': Func(1, func_even),
        'INT': Func(1, int),
        'ODD': Func(1, func_odd),
        'ROUND': Func(-1, round),
        'ROUNDDOWN': Func(-1, func_rounddown),
        'ROUNDUP': Func(-1, func_roundup),
        'TRUNC': Func(-1, func_trunc),

        # Random Numbers
        'RAND': Func(0, random.random),
        'RANDBETWEEN': Func(2, func_randbetween),

        # Trig
        'PI': Func(0, lambda: math.pi),
        'SQRTPI': Func(1, lambda a: math.sqrt(a) * math.pi),
        'DEGREES': Func(1, math.degrees),
        'RADIANS': Func(1, math.radians),
        'COS': Func(1, math.cos),
        'ACOS': Func(1, math.acos),
        'COSH': Func(1, math.cosh),
        'ACOSH': Func(1, math.acosh),
        'SIN': Func(1, math.sin),
        'ASIN': Func(1, math.asin),
        'SINH': Func(1, math.sinh),
        'ASINH': Func(1, math.asinh),
        'TAN': Func(1, math.tan),
        'ATAN': Func(1, math.atan),
        'ATAN2': Func(2, math.atan2),
        'TANH': Func(1, math.tanh),
        'ATANH': Func(1, math.atanh),

        # Exponents and Logarithms
        'EXP': Func(1, math.exp),
        'LN': Func(1, math.log),
        'LOG': Func(2, math.log),
        'LOG10': Func(1, math.log10),

        # Factorials
        'FACT': Func(1, func_factorial),
        'FACTDOUBLE': Func(1, func_double_factorial),

        # Averages
        'AVERAGE': Func(-1, func_average),
        'MEDIAN': Func(-1, func_median),
        'MODE': Func(-1, func_mode),
        'GEOMEAN': Func(-1, func_geomean),

        # Logical Functions
        'IF': Func(-2, func_if),
        'AND': Func(-1, wrap_varlist(all)),
        'OR': Func(-1, wrap_varlist(any)),
        'NOT': Func(1, operator.not_),
        'TRUE': Func(0, lambda: 1),
        'FALSE': Func(0, lambda: 0),
    }


def get_default_operators():
    """ generate a mapping of default operators allowed for evaluation """
    return {
        'u-': Func(1, operator.neg),             # unary negation
        'u%': Func(1, lambda a: a / float(100)), # unary percentage
        '+': Func(2, operator.add),
        '-': Func(2, operator.sub),
        '/': Func(2, operator.truediv),
        '*': Func(2, operator.mul),
        '=': Func(2, operator.eq),
        '<>': Func(2, lambda a, b: not operator.eq(a, b)),
        '>': Func(2, operator.gt),
        '<': Func(2, operator.lt),
        '>=': Func(2, operator.ge),
        '<=': Func(2, operator.le),
    }


def evaluate(formula, functions=None, operators=None):
    """
    evaluate an excel-style formula using the functions and operators provided

    """
    if functions is None:
        functions = get_default_functions()
    if operators is None:
        operators = get_default_operators()

    # first, parse the formula into reverse polish notation
    rpn = shunting_yard(formula)

    # check the nodes to make sure they are valid
    for i, n in enumerate(rpn):
        key = str(n).upper()
        if isinstance(n, RangeNode):
            if n.token.tsubtype not in ('logical', 'text'):
                raise Exception('Invalid Syntax: Only numeric values are allowed')
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
                raise Exception('Invalid Formula: {} requires {} arguments ({} provided)'.format(str(n), func.n, num))
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
                raise Exception('Invalid Formula: {} requires {} arguments ({} provided)'.format(str(n), op.n, num))
            stack, args = stack[:-num], stack[-num:]
            stack.append(op.f(*args))

    # if there's any stack left...the formula is invalid
    # all formulas should reduce to a single value
    if len(stack) > 1:
        raise Exception('Invalid Formula')

    return stack.pop()


class Func(object):
    """
    wrapper of a function and it's argument count

    if n > 0 then the function call requires n arguments
    if n =< 0 then the function call requires -n or more arguments
    """
    def __init__(self, n, f):
        self.n = n
        self.f = f


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
    raise Exception('Invalid Syntax: Only numeric values allowed ({} provided)'.format(n.token.tsubtype))


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


def func_if(test, true_value, *args):
    """ functor for ifs """
    false_value = args[0] if args else None
    return true_value if test else false_value


def func_lcm(a, b):
    """ functor for lowest common multiple """
    return a * b // fractions.gcd(a, b)


def func_sign(a):
    """ functor for sign """
    return 1 if a > 0 else -1 if a < 0 else 0


def func_ceil(a, factor=1):
    """ functor for ceiling with factor factor """
    return factor * math.ceil(float(a) / factor)


def func_floor(a, factor=1):
    """ functor for floor with factor factor """
    return factor * math.floor(float(a) / factor)


def func_even(a):
    """ functor for rounding up to next even integer """
    return func_ceil(a, 2)


def func_odd(a):
    """ functor for rounding up to next odd integer """
    if a % 2 == 1:
        return a
    return func_ceil(a, 2) + 1


def func_rounddown(a, places=0):
    """ functor for round down with decimal places """
    return math.floor(a * (10 ** places)) / float(10 ** places)


def func_roundup(a, places=0):
    """ functor for round up with decimal places """
    return math.ceil(a * (10 ** places)) / float(10 ** places)


def func_trunc(a, places=0):
    """ functor for truncate with decimals """
    return math.trunc(a * (10 ** places)) / float(10 ** places)


def func_randbetween(a, b):
    """ functor for random int in range """
    return a if a == b else random.randint(min(a, b), max(a, b))


def func_factorial(a):
    """ functor for a bounded factorial """
    if a > 170:
        raise Exception('Factorial limited to N <= 170')
    return math.factorial(a)


def func_double_factorial(a):
    """ functor for a bounded double factorial """
    if a > 288:
        raise Exception('Double factorial limited to N <= 288')
    return reduce(operator.mul, range(a, 0, -2), 1L)


def func_average(*args):
    """ functor for average of a series of numbers """
    return reduce(operator.add, args) / float(len(args))


def func_median(*args):
    """ functor for median of a series of numbers """
    data = sorted(args)
    n = len(data)
    if n % 2 == 1:
        return data[n // 2]
    else:
        i = n // 2
        return (data[i - 1] + data[i]) / 2.0


def func_mode(*args):
    """ functor for mode of a series of numbers """
    return collections.Counter(iter(args)).most_common(1)[0][0]


def func_geomean(*args):
    """ functor for geometric mean of a series of numbers """
    return (reduce(operator.mul, args)) ** (1.0 / len(args))


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
        input_field['help_text'] = 'Excel-style formula to evaluate. Example: `ROUNDUP(100.1231, 2) * 100`'
        return [input_field]

register(NumberFormulaTransform())
