import unittest
from botcenterdsl.parser import Parser


class ParserTestCase(unittest.TestCase):

    def test_balanced_parens(self):

        self.assertTrue(Parser.balanced_parens('()')[0])
        self.assertFalse(Parser.balanced_parens('(')[0])
        self.assertFalse(Parser.balanced_parens(')')[0])
        self.assertTrue(Parser.balanced_parens('(a)')[0])
        self.assertTrue(Parser.balanced_parens('[][]')[0])
        self.assertTrue(Parser.balanced_parens('(a [b] (c {d}))')[0])
        self.assertTrue(Parser.balanced_parens('(ab [c e (e) {a}] [d])')[0])
        self.assertFalse(Parser.balanced_parens('(a))')[0])
        self.assertFalse(Parser.balanced_parens('([][]}')[0])
        self.assertFalse(Parser.balanced_parens('{[[]}')[0])
        self.assertFalse(Parser.balanced_parens(')ab(')[0])

    def test_string_to_sexpr(self):

        self.assertEqual(Parser.string_to_sexpr('true'), True)

        sexpr = Parser.string_to_sexpr('(and true false)')
        self.assertEqual(sexpr, ['and', True, False])

        sexpr = Parser.string_to_sexpr('(+ (- 3 2) (sum 1 2 3 4))')
        self.assertEqual(sexpr, ['+', ['-', 3, 2], ['sum', 1, 2, 3, 4]])

        sexpr = Parser.string_to_sexpr('(f (g (h 2 3 4) "hola") i)')
        self.assertEqual(sexpr, ['f', ['g', ['h', 2, 3, 4], '"hola"'], 'i'])

        sexpr = Parser.string_to_sexpr("""
            {local
                [ (a 3) (b 2) ]
                (f a b)
            }
        """)
        self.assertEqual(sexpr, ['local', [['a', 3], ['b', 2]], ['f', 'a', 'b']])

        sexpr = Parser.string_to_sexpr('(define x "Holi, soy juanito")')
        self.assertEqual(len(sexpr), 3)
        self.assertEqual(sexpr[2], '"Holi, soy juanito"')

    def test_separate_sexpr_strings(self):

        code = """
            (define x 3)
            (define f (x) (+ x 4))
            (f x)
        """
        sexpr_strings = Parser.separate_sexpr_strings(code)
        self.assertEqual(len(sexpr_strings), 3)
        self.assertEqual(sexpr_strings[0], '(define x 3)')
        self.assertEqual(sexpr_strings[1], '(define f (x) (+ x 4))')
        self.assertEqual(sexpr_strings[2], '(f x)')

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
        bot_sexpr = Parser.string_to_sexpr(code)
        self.assertEqual(len(bot_sexpr), 3)
        result_sexpr = bot_sexpr[2]
        self.assertEqual(len(result_sexpr), 4)
        self.assertEqual(result_sexpr[0], 'node-result')
        self.assertEqual(result_sexpr[3], 'end-node')
