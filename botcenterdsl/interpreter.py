from botcenterdsl.environment import Environment
from botcenterdsl.evaluation.evaluator import Evaluator
from botcenterdsl.evaluation.values import BotNodeValue
from botcenterdsl.parser import Parser
from botcenterdsl.primitives import BotcenterDSLPrimitives


class WrappedException(Exception):

    def __init__(self, exception, execution_stack):

        self.wrapped = exception
        self.message = exception.message
        self.stack = execution_stack


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
            name: self.primitive_eval(code, evaluator)
            for name, code in self.code_definitions.items()
        })

    def primitive_eval(self, code_string, evaluator):

        ast_seq = Parser.parse(code_string)
        return self.interpret(ast_seq, evaluator)

    def eval(self, code_string):

        evaluator = Evaluator()
        self.evaluate_code_definitions(evaluator)
        return self.primitive_eval(code_string, evaluator)

    def eval_bot(self, bot_code, input_msg, evaluation_state=None):

        self.environment.add_primitives({
            'input-message': lambda: input_msg
        })
        evaluator = Evaluator(evaluation_state)
        self.evaluate_code_definitions(evaluator)
        result = self.primitive_eval(bot_code, evaluator)
        if isinstance(result, BotNodeValue):
            return result.apply(self.data)
        return result

    def interpret(self, ast_seq, evaluator):

        try:
            for ast in ast_seq[0:-1]:
                ast.accept(evaluator, self.environment)
            return ast_seq[-1].accept(evaluator, self.environment)
        except Exception as e:
            raise WrappedException(
                e,
                evaluator.execution_stack
            )

    @classmethod
    def run(cls, code_string, environment=None):

        return BotcenterDSL(environment).eval(code_string)
