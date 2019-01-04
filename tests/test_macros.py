from unittest import TestCase

from botlang import BotlangSystem, BotlangErrorException
from botlang.parser import BotLangSyntaxError


class MacrosTestCase(TestCase):

    def test_syntax_rule(self):

        code = """
        (define-syntax-rule (my-and x y)
            (if x
                (if y #t #f)
                #f
            )
        )
        (my-and (> 5 3) (< -1 8))
        """
        result = BotlangSystem.run(code)
        self.assertTrue(result)

    def test_defun_macro(self):

        code = """
        (define-syntax-rule (def-fun name args body)
            (define name (function args body))
        )
        (def-fun squared (x) (* x x))
        (squared 4)
        """
        result = BotlangSystem.run(code)
        self.assertEqual(result, 16)

    def test_macro_arguments_error(self):

        code = """
        (define-syntax-rule (def-fun name args body)
            (define name (function args body))
        )
        (def-fun times-ten (x)
            (define a 10)
            (* a x)
        )
        (times-ten 4)
        """
        with self.assertRaises(BotLangSyntaxError) as cm:
            BotlangSystem.run(code)
        self.assertTrue(
            'Expansion of macro def-fun failed' in cm.exception.args[0]
        )
        self.assertTrue(
            'expected 3 arguments, got 4' in cm.exception.args[0]
        )

    def test_syntax_rule_hygiene(self):

        code = """
        (define-syntax-rule (my-and x y)
            (if x
                (if y #t #f)
                #f
            )
        )
        (define y #t)
        (my-and y #f) ;; Yields #t if expansion is not hygienic
        """
        result = BotlangSystem.run(code)
        self.assertFalse(result)

    def test_dont_show_macro_source(self):

        code = """
        (defun f1 (x) (* 2 x))
        (defun f2 (x) (+ (f1 x) 4))
        (f2 nil)
        """
        with self.assertRaises(BotlangErrorException) as cm:
            BotlangSystem.run(code)
        stack_trace = cm.exception.print_stack_trace()
        self.assertFalse('(function args body)' in stack_trace)
