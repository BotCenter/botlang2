import unittest
from botlang.interpreter import BotlangSystem
from botlang.modules.resolver import ModuleResolver


class ModulesTestCase(unittest.TestCase):

    def test_module(self):

        module_resolver = ModuleResolver()
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

            (provide say-sentence)
            (provide say-cats)
        )
        """, module_resolver=module_resolver)
        self.assertEqual(module.name, 'my-module')

        bindings = module.get_bindings(module_resolver)
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
