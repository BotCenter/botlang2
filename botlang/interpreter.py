import inspect
import os

from botlang.environment import *
from botlang.evaluation.evaluator import Evaluator
from botlang.evaluation.values import BotNodeValue
from botlang.exceptions.exceptions import *
from botlang.extensions.cache import CacheExtension
from botlang.modules.resolver import ModuleResolver
from botlang.parser import Parser


class BotlangSystem(object):

    def __init__(self, environment=None, module_resolver=None):

        if not environment:
            environment = self.base_environment()

        if not module_resolver:
            module_resolver = ModuleResolver()

        self.environment = environment
        self.module_resolver = module_resolver

    @classmethod
    def base_environment(cls):

        env = Environment()
        return BotlangPrimitives.populate_environment(env)

    @classmethod
    def bot_modules_resolver(cls):

        from botlang.modules import bot_helpers
        helpers_path = os.path.dirname(inspect.getfile(bot_helpers))

        module_resolver = ModuleResolver()
        module_resolver.load_modules([
            '{0}/{1}'.format(helpers_path, 'helpers.bot')
        ])
        return module_resolver

    @classmethod
    def bot_instance(cls, module_resolver=None):

        environment = cls.base_environment()

        if module_resolver is None:
            module_resolver = cls.bot_modules_resolver()

        return BotlangSystem(environment, module_resolver)

    def setup_cache_extension(self, cache_implementation):

        return CacheExtension.enable_cache(self, cache_implementation)

    def primitive_eval(self, code_string, evaluator):

        ast_seq = Parser.parse(code_string)
        return self.interpret(ast_seq, evaluator, self.environment)

    def eval(self, code_string):

        evaluator = Evaluator(module_resolver=self.module_resolver)
        return self.primitive_eval(code_string, evaluator)

    def eval_bot(self, bot_code, input_msg, evaluation_state=None, data=None):

        if data is None:
            data = {}

        self.environment.add_cachable_primitives({
            'input-message': lambda: input_msg
        })
        evaluator = Evaluator(
            evaluation_state=evaluation_state,
            module_resolver=self.module_resolver
        )
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
    def run(cls, code_string, environment=None, module_resolver=None):

        return BotlangSystem(environment, module_resolver).eval(code_string)
