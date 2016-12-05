import unittest

from botlang import Evaluator
from botlang.interpreter import BotlangSystem
from botlang.modules.resolver import ModuleResolver


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
