# -*- coding: utf-8 -*-
import unittest
from botlang.parser import Parser, BotLangSyntaxError
from botlang.parser.bot_definition_checker import InvalidBotDefinitionException
from botlang.parser.s_expressions import Tree


class ParserTestCase(unittest.TestCase):

    def test_balanced_parens(self):

        self.assertTrue(Parser('(a)').s_expressions())
        self.assertTrue(Parser('[][]').s_expressions())
        self.assertTrue(Parser('(a [b] (c {d}))').s_expressions())
        self.assertTrue(Parser('(ab [c e (e) {a}] [d])').s_expressions())

        with self.assertRaises(BotLangSyntaxError) as cm:
            Parser('(a))').s_expressions()
        self.assertTrue('parentheses' in cm.exception.args[0])
        self.assertTrue('excess' in cm.exception.args[0])
        self.assertTrue('line 1' in cm.exception.args[0])

        self.assertRaises(
            BotLangSyntaxError,
            lambda: Parser('{[[]}').s_expressions()
        )
        self.assertRaises(
            BotLangSyntaxError,
            lambda: Parser(')ab(').s_expressions()
        )
        with self.assertRaises(BotLangSyntaxError) as cm:
            Parser("""
            (
                ([][]}
            )
            """).s_expressions()
        self.assertTrue("don't match, line 3" in cm.exception.args[0])

        with self.assertRaises(BotLangSyntaxError) as cm:
            Parser("""
            (define f (function (x)
                ((* x x)
            ))
            (f 4)
            """).s_expressions()
        self.assertTrue('not closed, line 6' in cm.exception.args[0])

        with self.assertRaises(BotLangSyntaxError) as cm:
            Parser("""
            (define f (function (x)
                (* x x)
            )))
            (f 4)
            """).s_expressions()
        self.assertTrue('excess' in cm.exception.args[0])
        self.assertTrue('line 4' in cm.exception.args[0])

    def test_comments(self):

        code = """
        ;; Hi, this is my kawaii code ;)

        (defun kawaii-function (❤)
            (append "(づ｡◕‿‿◕｡)づ kawaii desu ne " ❤) ; so kawaii <3
        )

        ;; yay
        (kawaii-function "(▰˘◡˘▰)") ;; (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
        (kawaii-function ";; (▰˘◡˘▰) ;;")
        """
        sexprs = Parser(code).s_expressions()
        self.assertEqual(len(sexprs), 3)
        self.assertEqual(sexprs[0].children[0].code, 'defun')
        self.assertEqual(sexprs[1].children[0].code, 'kawaii-function')
        self.assertEqual(sexprs[2].children[1].code, '";; (▰˘◡˘▰) ;;"')

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

    def test_symbols(self):

        code = """
        '(1 2 3)
        """
        list_expr = Parser(code).s_expressions()[0]
        self.assertTrue(list_expr.is_tree())
        self.assertTrue(list_expr.quoted)

    def test_strings(self):

        v = Parser('"Hola"').s_expressions()[0].to_ast()
        self.assertEqual(v.value, 'Hola')

        v = Parser('"λx:(μα.α→α).xx"').s_expressions()[0].to_ast()
        self.assertEqual(v.value, 'λx:(μα.α→α).xx')

        v = Parser('"Hola \\"Hola\\" Hola"').s_expressions()[0].to_ast()
        self.assertEqual(v.value, 'Hola "Hola" Hola')

        v = Parser('"\\n"').s_expressions()[0].to_ast()
        self.assertEqual(v.value, '\n')

        v = Parser('"\\u2063"').s_expressions()[0].to_ast()
        self.assertEqual(v.value, '\u2063')

        append = Parser(
            '(append "Asd \\"" "qwerty" "\\". sumthin")'
        ).s_expressions()[0].to_ast()
        self.assertEqual(append.arg_exprs[0].value, 'Asd "')
        self.assertEqual(append.arg_exprs[1].value, 'qwerty')
        self.assertEqual(append.arg_exprs[2].value, '". sumthin')

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
        self.assertEqual(sexpr[0].source_reference.start_line, 2)
        self.assertEqual(sexpr[0].source_reference.end_line, 2)
        self.assertEqual(sexpr[1].source_reference.start_line, 3)
        self.assertEqual(sexpr[1].source_reference.end_line, 3)
        self.assertEqual(sexpr[2].source_reference.start_line, 4)
        self.assertEqual(sexpr[2].source_reference.end_line, 4)

        code1 = "(+ 3 4)"
        sexpr = Parser(code1).s_expressions()
        self.assertEqual(len(sexpr), 1)
        self.assertEqual(sexpr[0].source_reference.start_line, 1)
        self.assertEqual(sexpr[0].source_reference.end_line, 1)

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
        self.assertEqual(node_sexpr.source_reference.start_line, 2)
        self.assertEqual(node_sexpr.source_reference.end_line, 8)

        args_sexpr = node_sexpr.children[1]
        result_sexpr = node_sexpr.children[2]
        botcito_sexpr = result_sexpr.children[2]
        end_node_sexpr = result_sexpr.children[3]

        self.assertEqual(args_sexpr.source_reference.start_line, 2)
        self.assertEqual(args_sexpr.source_reference.end_line, 2)

        self.assertEqual(result_sexpr.source_reference.start_line, 3)
        self.assertEqual(result_sexpr.source_reference.end_line, 7)

        self.assertEqual(botcito_sexpr.source_reference.start_line, 5)
        self.assertEqual(botcito_sexpr.source_reference.end_line, 5)

        self.assertEqual(end_node_sexpr.source_reference.start_line, 6)
        self.assertEqual(end_node_sexpr.source_reference.end_line, 6)

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

    def test_bot_definitions(self):

        code = """
            (bot-node (data)
                [define message (get [input-message] "message")]
                (node-result
                    data
                    (make-dict
                        (list
                            (cons "answer" message)
                        )
                    )
                    end-node
                )
            )
        """
        Parser.parse(code, None)

        code = """
            (module "a-bot-module"
                [define bot1 (bot-node (data) (node-result data "" end-node))]
                (provide bot1)
            )
        """
        Parser.parse(code, None)

        code = """
            (define bot1 (bot-node (data) (node-result data "" end-node)))
        """
        Parser.parse(code, None)

        code = """
            (function ()
                (bot-node (data) (node-result data "" end-node))
            )
        """
        self.assertRaises(
            InvalidBotDefinitionException,
            lambda: Parser.parse(code, None)
        )

        code = """
            (bot-node (data)
                [define bot2
                    (bot-node (data) (node-result data "" end-node))
                ]
                (bot2 data)
            )
        """
        self.assertRaises(
            InvalidBotDefinitionException,
            lambda: Parser.parse(code, None)
        )
