# -*- coding: utf-8 -*-
import unittest
from botcenterdsl.parser import Parser, BotLangSyntaxError
from botcenterdsl.parser.s_expressions import Tree


class ParserTestCase(unittest.TestCase):

    def test_balanced_parens(self):

        self.assertTrue(Parser('(a)').s_expressions())
        self.assertTrue(Parser('[][]').s_expressions())
        self.assertTrue(Parser('(a [b] (c {d}))').s_expressions())
        self.assertTrue(Parser('(ab [c e (e) {a}] [d])').s_expressions())

        self.assertRaises(
            BotLangSyntaxError,
            lambda: Parser('(a))').s_expressions()
        )
        self.assertRaises(
            BotLangSyntaxError,
            lambda: Parser('([][]}').s_expressions()
        )
        self.assertRaises(
            BotLangSyntaxError,
            lambda: Parser('{[[]}').s_expressions()
        )
        self.assertRaises(
            BotLangSyntaxError,
            lambda: Parser(')ab(').s_expressions()
        )

    def test_separate_sexpr_strings(self):

        code = """
            (define x 3)
            (define f (x) (+ x 4))
            (f x)
        """
        sexpr_strings = [
            sexpr.code for sexpr in Parser(code).s_expressions()
            ]
        self.assertEqual(len(sexpr_strings), 3)
        self.assertEqual(sexpr_strings[0], '(define x 3)')
        self.assertEqual(sexpr_strings[1], '(define f (x) (+ x 4))')
        self.assertEqual(sexpr_strings[2], '(f x)')

    def test_function_arguments(self):

        code = "(fun (n) (+ n 2))"
        fun_expr = Parser(code).s_expressions()[0]
        self.assertEqual(fun_expr.children[0].code, 'fun')

        args_expr = fun_expr.children[1]
        self.assertTrue(isinstance(args_expr, Tree))
        self.assertEqual(len(args_expr.children), 1)
        self.assertEqual(args_expr.children[0].code, 'n')

        code = "(fun (m n) (+ m n))"
        fun_expr = Parser(code).s_expressions()[0]
        args_expr = fun_expr.children[1]

        self.assertTrue(isinstance(args_expr, Tree))
        self.assertEqual(len(args_expr.children), 2)
        self.assertEqual(args_expr.children[0].code, 'm')
        self.assertEqual(args_expr.children[1].code, 'n')

    def test_bot_sexpr(self):

        code = """
            (bot-node (data)
                (node-result
                    data
                    (append "Holi, soy Botcito. " "Quien eres tu?")
                    end-node
                )
            )
        """
        bot_sexpr = Parser(code).s_expressions()
        self.assertEqual(len(bot_sexpr), 1)
        bot_node_sexpr = bot_sexpr[0].children
        self.assertEqual(len(bot_node_sexpr), 3)

        result_sexpr = bot_node_sexpr[2].children
        self.assertEqual(len(result_sexpr), 4)
        self.assertEqual(result_sexpr[0].code, 'node-result')
        self.assertEqual(result_sexpr[3].code, 'end-node')

    def test_lines_of_code(self):

        code = """
            (define x 3)
            (define f (x) (+ x 4))
            (f x)
        """
        sexpr = Parser(code).s_expressions()
        self.assertEqual(len(sexpr), 3)
        self.assertEqual(sexpr[0].start_line, 2)
        self.assertEqual(sexpr[0].end_line, 2)
        self.assertEqual(sexpr[1].start_line, 3)
        self.assertEqual(sexpr[1].end_line, 3)
        self.assertEqual(sexpr[2].start_line, 4)
        self.assertEqual(sexpr[2].end_line, 4)

        code1 = "(+ 3 4)"
        sexpr = Parser(code1).s_expressions()
        self.assertEqual(len(sexpr), 1)
        self.assertEqual(sexpr[0].start_line, 1)
        self.assertEqual(sexpr[0].end_line, 1)

        code2 = """
            (bot-node (data)
                (node-result
                    data
                    (append "Holi, soy Botcito. " "Quien eres tu?")
                    end-node
                )
            )
        """
        sexpr = Parser(code2).s_expressions()
        node_sexpr = sexpr[0]
        self.assertEqual(node_sexpr.start_line, 2)
        self.assertEqual(node_sexpr.end_line, 8)

        args_sexpr = node_sexpr.children[1]
        result_sexpr = node_sexpr.children[2]
        botcito_sexpr = result_sexpr.children[2]
        end_node_sexpr = result_sexpr.children[3]

        self.assertEqual(args_sexpr.start_line, 2)
        self.assertEqual(args_sexpr.end_line, 2)

        self.assertEqual(result_sexpr.start_line, 3)
        self.assertEqual(result_sexpr.end_line, 7)

        self.assertEqual(botcito_sexpr.start_line, 5)
        self.assertEqual(botcito_sexpr.end_line, 5)

        self.assertEqual(end_node_sexpr.start_line, 6)
        self.assertEqual(end_node_sexpr.end_line, 6)

    def test_code_string_information(self):

        code = """
        (some-function
            "String 1"
            3
            "String 2"
            "String 3"
            some-id
            "String 4"
        )
        """

        function_expr = Parser(code).s_expressions()[0]
        self.assertEqual(function_expr.children[1].code, '"String 1"')
        self.assertEqual(function_expr.children[2].code, '3')
        self.assertEqual(function_expr.children[3].code, '"String 2"')
        self.assertEqual(function_expr.children[4].code, '"String 3"')
        self.assertEqual(function_expr.children[5].code, 'some-id')
        self.assertEqual(function_expr.children[6].code, '"String 4"')
