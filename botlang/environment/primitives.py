from __future__ import print_function

import math
from functools import *
import operator as op
from collections import OrderedDict
from unidecode import unidecode

from botlang.evaluation.values import Nil, TerminalNode
from botlang.http.http_requests import *


def append(*values):
    return reduce(op.add, values)


def dict_put(ordered_dict, key, value):
    return OrderedDict(
        list(ordered_dict.items()) + [(key, value)]
    )


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


def cons(head, tail):

    if isinstance(tail, list):
        return [head] + tail
    return [head, tail]


def email_censor(value):
    if '@' not in value:
        return value
    start, end = value.split('@')
    return "{}@{}".format(
        word_censor(start),
        word_censor(end)
    )


def word_censor(value):
    if len(value) <= 1:
        return value
    half = int(len(value) / 2)
    censored = value[0:half] + '*' * (len(value) - half)
    return censored


def make_terminal_node(end_state):
    return TerminalNode(end_state)


class BotlangPrimitives(object):

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
        'fold': lambda v, f, l: reduce(f, l, v),
        'filter': lambda f, l: filter(f, l),
        'max': max,
        'min': min,
        'find': find_in_list,
        'cons': cons
    }

    DICT_OPERATIONS = {
        'make-dict': lambda bindings: OrderedDict(bindings),
        'put': dict_put,
        'get': dict_or_list_get,
        'associations': OrderedDict.items,
        'keys': OrderedDict.keys,
        'values': OrderedDict.values
    }

    PREDICATES = {
        'member?': lambda collection, element: element in collection,
        'starts-with?': str.startswith,
        'ends-with?': str.endswith,
        'contains?': str.__contains__
    }

    STRING_OPERATIONS = {
        'split': str.split,
        'plain': simplify_text,
        'email-censor': email_censor
    }

    TYPE_CONVERSION = {
        'str': str
    }

    SIDE_EFFECTS = {
        'print': print
    }

    TERMINAL_NODES = {
        'terminal-node': make_terminal_node
    }

    HTTP = {
        'http-get': http_get,
        'http-post': http_post
    }

    @classmethod
    def populate_environment(cls, environment):

        environment.update({'nil': Nil})
        environment.add_primitives(cls.MATH)
        environment.add_primitives(cls.UNARY_OPERATORS)
        environment.add_primitives(cls.BINARY_OPERATORS)
        environment.add_primitives(cls.LIST_OPERATIONS)
        environment.add_primitives(cls.DICT_OPERATIONS)
        environment.add_primitives(cls.PREDICATES)
        environment.add_primitives(cls.STRING_OPERATIONS)
        environment.add_primitives(cls.TYPE_CONVERSION)
        environment.add_primitives(cls.SIDE_EFFECTS)
        environment.add_primitives(cls.TERMINAL_NODES)
        environment.update({'end-node': make_terminal_node('BOT_ENDED')})
        environment.add_cachable_primitives(cls.HTTP)
        return environment
