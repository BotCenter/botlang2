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
            self.fail('Should not reach this')
        except BotlangErrorException as e:
            self.assertEqual(len(e.stack), 5)
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

    def test_primitives_exception(self):

        try:
            BotlangSystem().eval('(+ (list 1) #f)')
            self.fail('Should not reach this')
        except BotlangErrorException as e:
            self.assertEqual(len(e.stack), 1)
            print(e.print_stack_trace())
