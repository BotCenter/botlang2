import unittest

from botlang import BotlangSystem, BotlangErrorException


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
            BotlangSystem().eval(code)
        except BotlangErrorException as e:
            print(e.print_stack_trace())
            self.assertEqual(len(e.stack), 6)
            self.assertTrue(
                e.print_stack_trace().endswith('3 is not a function')
            )
            self.assertTrue(
                'line 8' in e.print_stack_trace()
            )
