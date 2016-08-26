from __future__ import print_function

import math
from functools import *
import operator as op
from collections import OrderedDict
from unidecode import unidecode

from botcenterdsl.evaluation.values import Nil


def append(*values):
    return reduce(op.add, values)


def dict_put(data_dict, key, value):
    data = data_dict.copy()
    data[key] = value
    return data


def dict_or_list_get(data_dict, key):
    return data_dict[key]


def dict_has_key(data_dict, key):
    try:
        return data_dict[key]
    except:
        return Nil


def find_in_list(find_function, lst):
    for elem in lst:
        if find_function(elem):
            return elem
    return Nil


def simplify_text(text):

    return unidecode(text)\
        .lower()\
        .replace("'", '')\
        .replace('&', '')


class BotcenterDSLPrimitives(object):

    MATH = vars(math)

    UNARY_OPERATORS = {
        'abs': abs,
        'not': op.not_,
        'nil?': lambda v: v is Nil
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
        'equal?': op.eq
    }

    LIST_OPERATIONS = {
        'append': append,
        'head': lambda x: x[0],
        'tail': lambda x: x[1:],
        'length': len,
        'list': lambda *x: list(x),
        'map': lambda f, l: list(map(f, l)),
        'reduce': lambda f, l: reduce(f, l),
        'max': max,
        'min': min,
        'in-list?': lambda lst, elem: elem in lst,
        'find': find_in_list
    }

    DICT_OPERATIONS = {
        'make-dict': lambda: OrderedDict(),
        'put': dict_put,
        'get': dict_or_list_get,
        'has-key': dict_has_key
    }

    STRING_OPERATIONS = {
        'plain': simplify_text
    }

    TYPE_CONVERSION = {
        'str': str
    }

    SIDE_EFFECTS = {
        'print': print
    }

    TERMINAL_NODE_STATES = {
        'end-node': 'BOT_ENDED'
    }

    @classmethod
    def populate_environment(cls, environment):

        environment.update({'nil': Nil})
        environment.add_primitives(cls.MATH)
        environment.add_primitives(cls.UNARY_OPERATORS)
        environment.add_primitives(cls.BINARY_OPERATORS)
        environment.add_primitives(cls.LIST_OPERATIONS)
        environment.add_primitives(cls.DICT_OPERATIONS)
        environment.add_primitives(cls.STRING_OPERATIONS)
        environment.add_primitives(cls.TYPE_CONVERSION)
        environment.add_primitives(cls.SIDE_EFFECTS)

        environment.add_terminal_nodes(cls.TERMINAL_NODE_STATES)
        return environment
