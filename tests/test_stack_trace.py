import unittest

from botcenterdsl import Parser, Evaluator, BotcenterDSL, WrappedException


class StackTraceTestCase(unittest.TestCase):

    def test_stack_trace(self):

        code = """
            (begin
                (define f
                    (fun (n)
                        (fun (x) (n x))
                    )
                )
                (define g (f 3))

                (+ (g 3) (g 2))
            )
        """
        ast = Parser.parse(code)
        try:
            BotcenterDSL().interpret(ast, Evaluator())
        except WrappedException as e:
            self.assertEqual(len(e.stack), 6)
