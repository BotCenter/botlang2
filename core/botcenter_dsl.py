from __future__ import print_function

import math
import operator as op

from core.environment import Environment
from core.evaluation.evaluator import Evaluator
from core.evaluation.values import BotNodeValue
from core.parser import Parser


def append(*values):
    return reduce(op.add, values)


def add_data(data_dict, key, value):
    data = data_dict.copy()
    data[key] = value
    return data


class BotcenterDSL(object):

    MATH_BINDINGS = vars(math)
    OP_BINDINGS = {
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': lambda x, y: x / y,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'abs': abs,
        'append': append,
        'equal?': op.eq,
        'head': lambda x: x[0],
        'tail': lambda x: x[1:],
        'length': len,
        'list': lambda *x: list(x),
        'map': lambda f, l: list(map(f, l)),
        'max': max,
        'min': min,
        'not': op.not_,
        'print': print,
        'add-data': add_data
    }

    def __init__(self, environment=None, bot_config=None):
        if not environment:
            environment = self.create_base_environment()
        self.data = {}
        self.environment = environment
        self.bot_config = bot_config
        if bot_config is not None:
            self.environment.add_primitives(bot_config.functions)

    def create_base_environment(self):
        env = Environment()
        env.add_primitives(self.MATH_BINDINGS)
        env.add_primitives(self.OP_BINDINGS)
        return env

    def eval(self, code_string):
        ast = Parser.parse(code_string)
        result = self.interpret(ast)
        if isinstance(result, BotNodeValue):
            return result.apply(self.data)
        return result

    def interpret(self, ast):
        return ast.accept(Evaluator(self), self.environment)

    def resume_execution(self, bot_node, data, input_msg):
        assert isinstance(bot_node, BotNodeValue)
        bot_node.env = bot_node.env.update({'input-message': input_msg})
        return bot_node.apply(data)

    def reached_bot_result(self, result):
        assert self.bot_config is not None
        return self.bot_config.result_hook(result)

    @classmethod
    def run(cls, code_string, environment=None):
        return BotcenterDSL(environment).eval(code_string)
