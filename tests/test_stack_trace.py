import unittest

from botcenterdsl import BotcenterDSL, BotLangException


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
        try:
            BotcenterDSL().eval(code)
        except BotLangException as e:
            self.assertEqual(len(e.stack), 6)
            self.assertTrue(
                e.print_stack_trace().endswith('3 is not a function')
            )
