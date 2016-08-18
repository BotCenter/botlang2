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
        self.code_definitions = {}

    @classmethod
    def base_environment(cls):

        env = Environment()
        return BotcenterDSLPrimitives.populate_environment(env)

    def add_code_definition(self, name, code):

        self.code_definitions[name] = code
        return self

    def evaluate_code_definitions(self, evaluator):

        return self.environment.update({
            name: Parser.parse(code).accept(evaluator, self.environment)
            for name, code in self.code_definitions.items()
        })

    def eval(self, code_string):

        ast = Parser.parse(code_string)
        evaluator = Evaluator()
        self.evaluate_code_definitions(evaluator)
        return self.interpret(ast, evaluator)

    def eval_bot(self, bot_code, input_msg, evaluation_state=None):

        self.environment.add_primitives({
            'input-message': lambda: input_msg
        })
        evaluator = Evaluator(evaluation_state)
        self.evaluate_code_definitions(evaluator)
        ast = Parser.parse(bot_code)
        result = self.interpret(ast, evaluator)
        if isinstance(result, BotNodeValue):
            return result.apply(self.data)
        return result

    def interpret(self, ast, evaluator=None):

        return ast.accept(evaluator, self.environment)

    @classmethod
    def run(cls, code_string, environment=None):

        return BotcenterDSL(environment).eval(code_string)
