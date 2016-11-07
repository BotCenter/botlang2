from botlang.environment import *
from botlang.environment.bot_helpers import BotHelpers
from botlang.evaluation.evaluator import Evaluator
from botlang.evaluation.values import BotNodeValue
from botlang.exceptions.exceptions import *
from botlang.extensions.cache import CacheExtension
from botlang.parser import Parser


class BotlangSystem(object):

    def __init__(self, environment=None):

        if not environment:
            environment = self.base_environment()
        self.environment = environment
        self.code_definitions = {}

    @classmethod
    def base_environment(cls):

        env = Environment()
        return BotlangPrimitives.populate_environment(env)

    @classmethod
    def bot_instance(cls):

        environment = cls.base_environment()
        dsl = BotlangSystem(environment)
        return BotHelpers.load_on_dsl(dsl)

    def add_code_definition(self, name, code):

        self.code_definitions[name] = code
        return self

    def evaluate_code_definitions(self, evaluator):

        return self.environment.update({
            name: self.primitive_eval(code, evaluator)
            for name, code in self.code_definitions.items()
        })

    def setup_cache_extension(self, cache_implementation):

        return CacheExtension.enable_cache(self, cache_implementation)

    def primitive_eval(self, code_string, evaluator):

        ast_seq = Parser.parse(code_string)
        return self.interpret(ast_seq, evaluator, self.environment)

    def eval(self, code_string):

        evaluator = Evaluator()
        self.evaluate_code_definitions(evaluator)
        return self.primitive_eval(code_string, evaluator)

    def eval_bot(self, bot_code, input_msg, evaluation_state=None, data=None):

        if data is None:
            data = {}

        self.environment.add_cachable_primitives({
            'input-message': lambda: input_msg
        })
        evaluator = Evaluator(evaluation_state)
        self.evaluate_code_definitions(evaluator)
        result = self.primitive_eval(bot_code, evaluator)
        if isinstance(result, BotNodeValue):
            return result.apply(data)
        return result

    @classmethod
    def interpret(cls, ast_seq, evaluator, environment):

        try:
            for ast in ast_seq[0:-1]:
                ast.accept(evaluator, environment)
            return ast_seq[-1].accept(evaluator, environment)
        except BotlangAssertionException as failed_assert:
            raise failed_assert
        except Exception as e:
            raise BotlangErrorException(
                e,
                evaluator.execution_stack
            )

    @classmethod
    def run(cls, code_string, environment=None):

        return BotlangSystem(environment).eval(code_string)
