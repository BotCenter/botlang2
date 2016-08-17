import unittest

from botcenterdsl.interpreter import BotcenterDSL
from botcenterdsl.evaluation.evaluator import Primitive
from botcenterdsl.evaluation.values import BotResultValue


class BotcenterDSLTestCase(unittest.TestCase):

    def test_primitive_values(self):

        self.assertTrue(BotcenterDSL.run('true'))
        self.assertFalse(BotcenterDSL.run('false'))
        self.assertEqual(BotcenterDSL.run('2'), 2)
        self.assertEqual(BotcenterDSL.run('3.14'), 3.14)
        self.assertEqual(BotcenterDSL.run('"hola"'), "hola")

    def test_and(self):

        self.assertTrue(BotcenterDSL.run('(and true true)'))
        self.assertFalse(BotcenterDSL.run('(and true false)'))
        self.assertFalse(BotcenterDSL.run('(and false true)'))
        self.assertFalse(BotcenterDSL.run('(and false false)'))

    def test_or(self):

        self.assertTrue(BotcenterDSL.run('(or true true)'))
        self.assertTrue(BotcenterDSL.run('(or true false)'))
        self.assertTrue(BotcenterDSL.run('(or false true)'))
        self.assertFalse(BotcenterDSL.run('(or false false)'))

    def test_if(self):

        self.assertEqual(BotcenterDSL.run('(if true 2 3)'), 2)
        self.assertEqual(BotcenterDSL.run('(if false 2 3)'), 3)
        self.assertEqual(BotcenterDSL.run('(if (> 4 5) 100 200)'), 200)

    def test_primitive_application(self):

        self.assertTrue(BotcenterDSL.run('(not false)'))
        self.assertEqual(BotcenterDSL.run('(sqrt 4)'), 2)
        self.assertEqual(BotcenterDSL.run('(* 5 (/ 10 2))'), 25)
        self.assertEqual(BotcenterDSL.run('(list 3 4 5 2 1)'), [3, 4, 5, 2, 1])
        self.assertEqual(BotcenterDSL.run('(max (list 3 4 5 2 1))'), 5)
        self.assertEqual(BotcenterDSL.run('(min (list 3 4 5 2 1))'), 1)
        self.assertEqual(BotcenterDSL.run('(map abs (list 1 -2 3))'), [1, 2, 3])

    def test_closures(self):

        self.assertTrue(BotcenterDSL.run('((fun (x) x) true)'))
        self.assertEqual(BotcenterDSL.run(
            '((fun (x y) (+ (* x x) (* y y))) 3 4)'
        ), 25)

    def test_environment(self):

        runtime = BotcenterDSL()
        bindings = {
            'x': 4,
            'hola': BotcenterDSL.run('(max (list 1 3 2))'),
            '+': Primitive(lambda x, y: x * y, runtime.environment)
        }
        new_env = runtime.environment.new_environment(bindings)

        self.assertEqual(BotcenterDSL.run('(- 3 x)', new_env), -1)
        self.assertEqual(BotcenterDSL.run('(- 10 hola)', new_env), 7)
        self.assertEqual(BotcenterDSL.run('(+ 2 3)', new_env), 6)

    def test_add_python_functions(self):

        def fibonacci(n):
            assert n >= 0

            if n == 0:
                return 0
            if n == 1:
                return 1
            return fibonacci(n - 1) + fibonacci(n - 2)

        runtime = BotcenterDSL()
        runtime.environment.add_primitives({'fibo': fibonacci})
        self.assertEqual(runtime.eval('(fibo 4)'), 3)
        self.assertEqual(runtime.eval('(fibo 7)'), 13)

    def test_nesting(self):

        code = """
            (if (> (* 0.3 (+ 10 23)) 10)
                esto-no-sera-evaluado-asi-que-pico
                (and
                     (= (head (map abs (list -1 -2 -3))) 1)
                     (<= 11 (/ 100 6))
                )
             )
        """
        self.assertTrue(BotcenterDSL.run(code))

    def test_define(self):

        code = """
            (define x 2)
            (define y 3)
            (+ x y)
        """
        self.assertEqual(BotcenterDSL.run(code), 5)

        code = """
            (define factorial
                (fun (n)
                    (if (equal? n 0)
                        1
                        (* n (factorial (- n 1)))
                    )
                )
            )
            (factorial 5)
        """
        self.assertEqual(BotcenterDSL.run(code), 120)

    def test_begin(self):

        code = """
            (begin
                (define x 1)
                (define y 2)
                (+ x y)
            )
        """
        self.assertEqual(BotcenterDSL.run(code), 3)

    def test_local_definitions(self):

        code = """
            (local
                (
                    (f (fun (x y) (* x y)))
                    (x (* 2 3))
                )
                (f x 2)
            )
        """
        self.assertEqual(BotcenterDSL.run(code), 12)

    def test_recursion(self):

        code = """
            (local
                ((factorial
                    (fun (n)
                        (if (equal? n 1)
                            n
                            (* n (factorial (- n 1)))
                        )
                    )
                ))
                (factorial 5)
            )
        """
        self.assertEqual(BotcenterDSL.run(code), 120)

    def test_first_order_functions(self):

        code = """
            (begin
                (define f
                    (fun (n)
                        (fun (x) (+ n x))
                    )
                )
                (define g (f 3))

                (+ (g 3) (g 2))
            )
        """
        self.assertEqual(BotcenterDSL.run(code), 11)

    def test_bot_node(self):

        code = """
            (bot-node (data)
                (node-result
                    data
                    "Holi, soy Botcito"
                    end-node
                )
            )
        """
        test = {'value': 0}
        self.assertEqual(test['value'], 0)

        node_result = BotcenterDSL(
            BotcenterDSL.base_environment().add_primitives(
                {'end-node': (lambda: test.update(value=1))}
            )
        ).eval_bot(code, 'mensaje inicial')
        self.assertTrue(isinstance(node_result, BotResultValue))
        self.assertTrue(isinstance(node_result.data, dict))
        self.assertEqual(node_result.message, 'Holi, soy Botcito')
        self.assertEqual(test['value'], 1)

    def test_evaluation_state(self):

        test_dict = {'value': 0}

        def test_primitive():
            test_dict['value'] += 1
            return 'holi'

        code = """
            (bot-node (data)
                (test-primitive)
                (test-primitive)
                (node-result
                    data
                    "Holi"
                    (bot-node (data)
                        (test-primitive)
                        (node-result
                            data
                            "Chau"
                            end-node
                        )
                    )
                )
            )
        """

        environment = BotcenterDSL.base_environment().add_primitives(
            {
                'test-primitive': test_primitive,
                'end-node': lambda: 'fin'
            }
        )
        first_node_result = BotcenterDSL(environment).eval_bot(code, 'oli bot')
        self.assertEqual(first_node_result.message, 'Holi')
        self.assertEqual(test_dict['value'], 2)

        execution_state = first_node_result.execution_state
        bot_node_steps = execution_state.bot_node_steps
        primitives_evaluations = execution_state.primitives_values
        self.assertEqual(bot_node_steps, 1)
        self.assertEqual(len(primitives_evaluations), 2)

        second_node_result = BotcenterDSL(environment).eval_bot(
            code,
            'otro mensaje',
            execution_state
        )
        self.assertEqual(second_node_result.message, 'Chau')
        self.assertEqual(test_dict['value'], 3)

        execution_state = second_node_result.execution_state
        bot_node_steps = execution_state.bot_node_steps
        primitives_evaluations = execution_state.primitives_values
        self.assertEqual(bot_node_steps, 2)
        self.assertEqual(len(primitives_evaluations), 3)

    def test_add_code_definition(self):

        environment = BotcenterDSL.base_environment()
        environment.add_code_definition('f', '(fun (n) [fun (x) (+ n x)])')
        code = """
            (begin
                (define g (f 3))

                (+ (g 3) (g 2))
            )
        """
        self.assertEqual(BotcenterDSL.run(code, environment), 11)
