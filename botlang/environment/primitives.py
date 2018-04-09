import base64
import bz2
import math
import re
from functools import *
import operator as op
from collections import OrderedDict
from uuid import uuid4
from urllib.parse import quote

import time
from unidecode import unidecode

from botlang.evaluation.values import Nil, TerminalNode
from botlang.http.http_requests import *


def append(*values):
    return reduce(op.add, values)


def extend(lst, value):
    if isinstance(value, list):
        return lst + value
    return lst + [value]


def dict_put(ordered_dict, key, value):
    return OrderedDict(
        list(ordered_dict.items()) + [(key, value)]
    )


def get_or_nil(data_struct, key):
    try:
        return data_struct[key]
    except KeyError:
        return Nil
    except IndexError:
        return Nil


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


def sort_function(comparator_function, lst):
    cmp_fun = lambda a, b: -1 if comparator_function(a, b) else 1
    return list(sorted(lst, key=cmp_to_key(cmp_fun)))


def base64_encode(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')


def base64_decode(text):
    return base64.b64decode(text.encode('utf-8')).decode('utf-8')


def make_dict(bindings):
    return OrderedDict(bindings)


def any_satisfy(fun, lst):
    for e in lst:
        if fun(e):
            return True
    return False


def pattern_match(pattern, message):
    if re.match(pattern, message):
        return True
    return False


def divide_text(max_chars, text):

    if len(text) <= max_chars:
        return [text]

    texts = []
    for p in re.split('\n', text):
        stripped_p = p.strip()
        if len(stripped_p) > 0:
            texts.append(stripped_p)

    return texts


class BotlangPrimitives(object):

    MATH = {
        'acos': math.acos,
        'acosh': math.acosh,
        'asin': math.asin,
        'asinh': math.asinh,
        'atan': math.atan,
        'atan2': math.atan2,
        'atanh': math.atanh,
        'ceil': math.ceil,
        'copysign': math.copysign,
        'cos': math.cos,
        'cosh': math.cosh,
        'degrees': math.degrees,
        'e': math.e,
        'erf': math.erf,
        'erfc': math.erfc,
        'exp': math.exp,
        'expm1': math.expm1,
        'fabs': math.fabs,
        'factorial': math.factorial,
        'floor': math.floor,
        'fmod': math.fmod,
        'frexp': math.frexp,
        'fsum': math.fsum,
        'gamma': math.gamma,
        'gcd': math.gcd,
        'hypot': math.hypot,
        'inf': math.inf,
        'close?': math.isclose,
        'finite?': math.isfinite,
        'inf?': math.isinf,
        'nan?': math.isnan,
        'ldexp': math.ldexp,
        'lgamma': math.lgamma,
        'log': math.log,
        'log10': math.log10,
        'log1p': math.log1p,
        'log2': math.log2,
        'modf': math.modf,
        'nan': math.nan,
        'pi': math.pi,
        'pow': math.pow,
        'radians': math.radians,
        'round': round,
        'sin': math.sin,
        'sinh': math.sinh,
        'sqrt': math.sqrt,
        'tan': math.tan,
        'tanh': math.tanh,
        'trunc': math.trunc
    }

    UNARY_OPERATORS = {
        'abs': abs,
        'not': op.not_,
        'nil?': lambda v: v is Nil or v is None
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

    LIST_OPERATIONS = {
        'append': append,
        'extend': extend,
        'head': lambda x: x[0],
        'tail': lambda x: x[1:],
        'init': lambda x: x[:-1],
        'last': lambda x: x[-1],
        'length': len,
        'list': lambda *x: list(x),
        'map': lambda f, l: list(map(f, l)),
        'reduce': lambda f, l: reduce(f, l),
        'fold': lambda v, f, l: reduce(f, l, v),
        'filter': lambda f, l: list(filter(f, l)),
        'sort': sort_function,
        'max': max,
        'min': min,
        'find': find_in_list,
        'cons': cons,
        'reverse': lambda l: l[::-1],
        'enumerate': lambda l: list(enumerate(l)),
        'sum': sum,
        'list?': lambda l: isinstance(l, list)
    }

    DICT_OPERATIONS = {
        'make-dict': make_dict,
        'put': dict_put,
        'put!': dict.__setitem__,
        'get': dict_or_list_get,
        'get-or-nil': get_or_nil,
        'associations': OrderedDict.items,
        'keys': OrderedDict.keys,
        'values': OrderedDict.values
    }

    PREDICATES = {
        'member?': lambda collection, element: element in collection,
        'starts-with?': str.startswith,
        'ends-with?': str.endswith,
        'contains?': str.__contains__,
        'any-satisfy?': any_satisfy
    }

    STRING_OPERATIONS = {
        'split': str.split,
        'join': str.join,
        'plain': simplify_text,
        'email-censor': email_censor,
        'uppercase': str.upper,
        'lowercase': str.lower,
        'capitalize': str.capitalize,
        'replace': str.replace,
        'trim': str.strip,
        'match?': pattern_match,
        'divide-text': divide_text,
        'url-quote': quote
    }

    TYPE_CONVERSION = {
        'str': str,
        'num': float,
        'int': int
    }

    # SIDE_EFFECTS = {
    #     'print': print
    # }

    TERMINAL_NODES = {
        'terminal-node': make_terminal_node
    }

    HTTP = {
        'http-get': http_get,
        'http-post': http_post
    }

    BASE64 = {
        'b64-encode': base64_encode,
        'b64-decode': base64_decode
    }

    RANDOM = {
        'uuid': uuid4
    }

    DATETIME = {
        'timestamp': time.time
    }

    COMPRESSION = {
        'bz2-compress': lambda string: base64.b64encode(
            bz2.compress(string.encode('utf-8'))
        ).decode('ascii'),
        'bz2-decompress': lambda b64_string: bz2.decompress(
            base64.b64decode(b64_string.encode('ascii'))
        ).decode('utf-8')
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
        # environment.add_primitives(cls.SIDE_EFFECTS)
        environment.add_primitives(cls.TERMINAL_NODES)
        environment.add_primitives(cls.BASE64)
        environment.add_primitives(cls.COMPRESSION)
        environment.add_primitives(cls.RANDOM)
        environment.add_primitives(cls.DATETIME)
        environment.update({'end-node': make_terminal_node('BOT_ENDED')})
        environment.add_primitives({
            'input-message': environment.get_last_input_message
        })
        environment.add_primitives(cls.HTTP)
        return environment
