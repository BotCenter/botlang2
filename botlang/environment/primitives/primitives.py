import operator as op


from botlang.environment.primitives import math, http, collections, \
    compression, base64, random, datetime, reflection, exceptions, oop
from botlang.environment.primitives.strings import string_functions
from botlang.evaluation.values import Nil, TerminalNode


def make_terminal_node(end_state):
    return TerminalNode(end_state)


def any_satisfy(fun, lst):
    for e in lst:
        if fun(e):
            return True
    return False


class BotlangPrimitives(object):

    UNARY_OPERATORS = {
        'not': op.not_
    }

    BINARY_OPERATORS = {
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': lambda x, y: x / y,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'equal?': op.eq,
        'mod': op.mod
    }

    PREDICATES = {
        'member?': lambda collection, element: element in collection,
        'starts-with?': str.startswith,
        'ends-with?': str.endswith,
        'contains?': str.__contains__,
        'any-satisfy?': any_satisfy
    }

    TYPE_CONVERSION = {
        'str': str,
        'num': float,
        'int': int
    }

    TYPE_CHECKING = {
        'nil?': lambda v: v is Nil or v is None,
        'bool?': lambda b: isinstance(b, bool),
        'str?': lambda s: isinstance(s, str),
        'num?': lambda n:
            isinstance(n, (float, int)) and not isinstance(n, bool),
        'int?': lambda i: isinstance(i, int) and not isinstance(i, bool),
        'list?': lambda l: isinstance(l, list)
    }

    TERMINAL_NODES = {
        'terminal-node': make_terminal_node
    }

    PRIMITIVE_GROUPS = [
        UNARY_OPERATORS,
        BINARY_OPERATORS,
        PREDICATES,
        TYPE_CONVERSION,
        TYPE_CHECKING,
        TERMINAL_NODES,

        string_functions.STRING_OPS,
        collections.COMMON_OPERATIONS,
        collections.DICT_OPERATIONS,
        collections.LIST_OPERATIONS,
        math.MATH_PRIMITIVES,
        random.RANDOM_PRIMITIVES,
        datetime.DATETIME_PRIMITIVES,
        http.HTTP_PRIMITIVES,
        base64.EXPORT_FUNCTIONS,
        compression.EXPORT_FUNCTIONS,
        exceptions.EXCEPTION_PRIMITIVES,
        oop.OOP_PRIMITIVES
    ]

    @classmethod
    def populate_environment(cls, environment):

        environment.update({'nil': Nil})

        for primitives_group in cls.PRIMITIVE_GROUPS:
            environment.add_primitives(primitives_group)

        environment.update({'end-node': make_terminal_node('BOT_ENDED')})
        environment.add_primitives({
            'input-message': environment.get_last_input_message     # Legacy
        })
        environment.add_reflective_primitives(reflection.REFLECTIVE_PRIMITIVES)

        return environment
