import unittest

from botlang import Evaluator
from botlang.interpreter import BotlangSystem
from botlang.modules.module import ExternalModule
from botlang.modules.resolver import ModuleResolver
from botlang.parser import BotLangSyntaxError
from tests.test_macros import MacrosTestCase


class ModulesTestCase(unittest.TestCase):

    def test_module(self):

        module_resolver = ModuleResolver(BotlangSystem.base_environment())
        module = BotlangSystem.run("""
        (module "my-module"
            [define say-cats
                (function () "cats")
            ]
            [define say-i-like
                (function () "i like")
            ]
            [define say-sentence
                (function () (append (say-i-like) " " (say-cats)))
            ]

            (provide
                say-sentence
                say-cats
            )
        )
        """, module_resolver=module_resolver)
        self.assertEqual(module.name, 'my-module')

        bindings = module.get_bindings(
            Evaluator(module_resolver=module_resolver)
        )
        self.assertEqual(len(bindings.items()), 2)
        self.assertFalse(bindings.get('say-sentence') is None)
        self.assertFalse(bindings.get('say-cats') is None)
        self.assertTrue(bindings.get('say-i-like') is None)

        code = """
        (require "my-module")
        (say-sentence)
        """
        result = BotlangSystem.run(code, module_resolver=module_resolver)
        self.assertEqual(result, "i like cats")
        #
        # code = """
        # (require "my-module")
        # (say-i-like)
        # """
        # result = BotlangSystem.run(code, module_resolver=module_resolver)
        # self.assertTrue('not defined' in result)

    def test_class_defined_in_module(self):

        pass

    def test_modules_resolver(self):

        resolver = BotlangSystem.bot_modules_resolver(
            BotlangSystem.base_environment()
        )
        valid_rut = BotlangSystem.run(
            '(require "bot-helpers") (validate-rut "16926695-6")',
            module_resolver=resolver
        )
        self.assertTrue(valid_rut)

        invalid_rut = BotlangSystem.run(
            '(require "bot-helpers") (validate-rut "16926695-5")',
            module_resolver=resolver
        )
        self.assertFalse(invalid_rut)

    def test_external_modules(self):

        external_module = ExternalModule(
            'cool-module',
            {
                'moo': lambda: 'moo',
                'meow': lambda: 'mew'
            }
        )
        environment = BotlangSystem.base_environment()
        resolver = ModuleResolver(environment)
        resolver.add_module(external_module)
        meow = BotlangSystem.run(
            '(require "cool-module") (meow)',
            module_resolver=resolver
        )
        self.assertEqual(meow, 'mew')

    # def test_circular_dependencies(self):
    #
    #     module_resolver = ModuleResolver(BotlangSystem.base_environment())
    #     BotlangSystem.run("""
    #     (module "mod1"
    #         (require "mod2")
    #         [define say-cats (function () "cats")]
    #         (provide say-cats)
    #     )
    #     """, module_resolver=module_resolver)
    #
    #     BotlangSystem.run("""
    #     (module "mod2"
    #         (require "mod1")
    #         [define say-dogs (function () "dogs")]
    #         (provide say-dogs)
    #     )
    #     """, module_resolver=module_resolver)
    #
    #     bot_code = '(require "mod1") (say-cats)'
    #
    #     self.assertEqual(
    #         BotlangSystem.run(bot_code, module_resolver=module_resolver),
    #         'cats'
    #     )
