from botcenterdsl.environment import Environment
from botcenterdsl.evaluation.evaluator import Evaluator
from botcenterdsl.evaluation.values import BotNodeValue
from botcenterdsl.parser import Parser
from botcenterdsl.primitives import BotcenterDSLPrimitives


class BotcenterDSL(object):

    def __init__(self, environment=None):

        if not environment:
            environment = self.base_environment()
        self.data = {}
        self.environment = environment

    @classmethod
    def base_environment(cls):

        env = Environment()
        return BotcenterDSLPrimitives.populate_environment(env)

    def eval(self, code_string):

        ast = Parser.parse(code_string)
        return self.interpret(ast)

    def eval_bot(self, bot_code, input_msg, evaluation_state=None):

        ast = Parser.parse(bot_code)
        result = self.interpret(ast, input_msg, evaluation_state)
        if isinstance(result, BotNodeValue):
            return result.apply(self.data)
        return result

    def interpret(self, ast, input_msg=None, evaluation_state=None):
        if input_msg is not None:
            self.environment.add_primitives({
                'input-message': lambda: input_msg
            })
        return ast.accept(Evaluator(evaluation_state), self.environment)

    @classmethod
    def run(cls, code_string, environment=None):

        return BotcenterDSL(environment).eval(code_string)
