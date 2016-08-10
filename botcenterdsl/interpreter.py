from __future__ import print_function

import math
import operator as op

from botcenterdsl.environment import Environment
from botcenterdsl.evaluation.evaluator import Evaluator
from botcenterdsl.evaluation.values import BotNodeValue
from botcenterdsl.node_hasher import NodeHasher
from botcenterdsl.parser import Parser


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

    def __init__(self, environment=None):

        if not environment:
            environment = self.create_base_environment()
        self.data = {}
        self.environment = environment
        self.ast_nodes = None

    @classmethod
    def create_base_environment(cls):

        env = Environment()
        env.add_primitives(cls.MATH_BINDINGS)
        env.add_primitives(cls.OP_BINDINGS)
        return env

    def eval(self, code_string):

        ast = Parser.parse(code_string)
        return self.interpret(ast)

    def eval_bot(self, bot_code):

        ast = Parser.parse(bot_code)
        nodes_hasher = NodeHasher()
        ast.accept(nodes_hasher, None)
        self.ast_nodes = nodes_hasher.ast_nodes
        result = self.interpret(ast)
        if isinstance(result, BotNodeValue):
            return result.apply(self.data)
        return result

    def interpret(self, ast):
        return ast.accept(Evaluator(self), self.environment)

    def resume_execution(self, bot_stub, bindings, data, input_msg):

        bot_node = self.ast_nodes.get(bot_stub['node_id'])
        environment = Environment(bindings=bindings)
        bot_node_closure = bot_node.accept(Evaluator(self), environment)
        return self.execute_from_node(bot_node_closure, data, input_msg)

    @classmethod
    def execute_from_node(cls, bot_node, data, input_msg):

        assert isinstance(bot_node, BotNodeValue)
        bot_node.env = bot_node.env.update({'input-message': input_msg})
        return bot_node.apply(data)

    @classmethod
    def run(cls, code_string, environment=None):

        return BotcenterDSL(environment).eval(code_string)
