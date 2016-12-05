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
            self.assertEqual(len(e.stack), 4)
            self.assertTrue(
                e.print_stack_trace().endswith('3 is not a function')
            )
            self.assertTrue(
                'line 5' in e.print_stack_trace()
            )

        code = """
            [define API_KEY "Yzy4kaJjPsWz7LVRB6Q86GcnJX9SvxaC"]
            [define ACCESS_HEADERS
                (make-dict
                    (list
                        (cons "Content-Type" "application/json")
                        (cons "ApiKey" API_KEY)
                    )
                )
            ]
            (non-existent-function 1)
        """
        try:
            BotlangSystem().eval(code)
        except BotlangErrorException as e:
            self.assertEqual(len(e.stack), 2)
