import inspect
import os

from botlang.environment import *
from botlang.evaluation.evaluator import Evaluator
from botlang.evaluation.values import BotNodeValue
from botlang.exceptions.exceptions import *
from botlang.extensions.storage import LocalStorageExtension, \
    GlobalStorageExtension, CacheExtension
from botlang.macros.macro_expander import MacroExpander
from botlang.modules.resolver import ModuleResolver
from botlang.parser import Parser


class BotlangSystem(object):

    def __init__(self, environment=None, module_resolver=None):

        if module_resolver:
            environment = module_resolver.environment

        if not environment:
            environment = self.base_environment()

        if not module_resolver:
            module_resolver = ModuleResolver(environment)

        self.environment = environment
        self.module_resolver = module_resolver

    @classmethod
    def base_environment(cls):

        env = Environment()
        return BotlangPrimitives.populate_environment(env)

    @classmethod
    def bot_modules_resolver(cls, environment):

        from botlang.modules import bot_helpers
        helpers_path = os.path.dirname(inspect.getfile(bot_helpers))

        module_resolver = ModuleResolver(environment)
        module_resolver.load_modules(helpers_path)
        return module_resolver

    @classmethod
    def bot_instance(cls, module_resolver=None):

        environment = cls.base_environment()

        if module_resolver is None:
            module_resolver = cls.bot_modules_resolver(environment)

        return BotlangSystem(module_resolver=module_resolver)

    def setup_cache_extension(self, cache_implementation):

        return CacheExtension.apply(self, cache_implementation)

    def setup_local_storage(self, db_implementation):

        return LocalStorageExtension.apply(self, db_implementation)

    def setup_global_storage(self, db_implementation):

        return GlobalStorageExtension.apply(self, db_implementation)

    def expand_macros(self, ast, macro_environment):

        return ast.accept(MacroExpander(), macro_environment)

    def primitive_eval(self, code_string, evaluator, source_id):

        ast_seq = Parser.parse(code_string, source_id)
        macro_environment = Environment()
        expanded_asts = [
            self.expand_macros(ast, macro_environment) for ast in ast_seq
        ]
        return self.interpret(expanded_asts, evaluator, self.environment)

    def eval(self, code_string, source_id=None):

        evaluator = Evaluator(module_resolver=self.module_resolver)
        return self.primitive_eval(code_string, evaluator, source_id)

    def eval_bot(
            self,
            bot_code,
            input_msg,
            evaluation_state=None,
            data=None,
            source_id=None
    ):
        if data is None:
            data = {}

        self.environment.last_input_message = input_msg
        evaluator = Evaluator(
            evaluation_state=evaluation_state,
            module_resolver=self.module_resolver
        )
        result = self.primitive_eval(bot_code, evaluator, source_id)
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
    def run(
            cls,
            code_string,
            environment=None,
            module_resolver=None,
            source_id=None
    ):
        return BotlangSystem(environment, module_resolver).eval(
            code_string,
            source_id
        )
