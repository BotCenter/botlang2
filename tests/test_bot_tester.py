# -*- coding: utf-8 -*-
from unittest import TestCase

from botlang.examples.example_bots import ExampleBots
from botlang.testing.bot_tester import BotlangTester


class BotlangTesterTestCase(TestCase):

    bot_code = ExampleBots.dog_bot_code

    def test_full_bot(self):

        tests_code = """
            (define test-bot
                [function (bot)
                    [define r2 (send-message bot "hola")]
                    (assert (starts-with? (get r2 'message) "Bienvenido a Botcenter!"))

                    [define r3 (send-message (get r2 'bot) "Juanito")]
                    (assert-equal? (get r3 'message) "Mucho gusto Juanito. Indíqueme su RUT, por favor.")

                    [define r4 (send-message (get r3 'bot) "17098131-2")]
                    (assert (ends-with? (get r4 'message) "Intente nuevamente."))

                    [define r5 (send-message (get r4 'bot) "16926695-6")]
                    (assert (contains? (get r5 'message) "¿Tiene perro?"))

                    [define r6 (send-message (get r5 'bot) "bla")]
                    (assert (starts-with? (get r6 'message) "Debe responder si o no."))

                    [define r7 (send-message (get r6 'bot) "no")]
                    (assert-equal? (get r7 'message) "Miau, Juanito :3")

                    [define r8 (send-message (get r6 'bot) "si")]
                    (assert-equal? (get r8 'message) "Wauf, Juanito!")
                ]
            )
        """
        results = BotlangTester.run(self.bot_code, tests_code)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].is_success())

    def test_setup(self):

        tests_code = """
            (define setup-node-to-test
                [function (bot)
                    [define node2 (send-message bot "hola")]
                    [define node3 (send-message (get node2 'bot) "Pepe")]
                    [define node4 (send-message (get node3 'bot) "16926695-6")]
                    (get node4 'bot)
                ]
            )
            (define test-1
                [function (bot)
                    (assert-equal?
                        [get (send-message node-to-test "bla") 'message]
                        "Debe responder si o no. ¿Tiene perro?"
                    )
                ]
            )
            (define test-2
                [function (bot)
                    (assert-equal?
                        [get (send-message node-to-test "no") 'message]
                        "Miau, Pepe :3"
                    )
                ]
            )
            (define test-3
                [function (bot)
                    (assert-equal?
                        [get (send-message node-to-test "si") 'message]
                        "Wauf, Pepe!"
                    )
                ]
            )
        """
        results = BotlangTester.run(self.bot_code, tests_code)
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].is_success())
        self.assertTrue(results[1].is_success())
        self.assertTrue(results[2].is_success())

    def test_results(self):

        tests_code = """
            (define test-bot
                [function (bot)
                    [define r (send-message bot "hola")]
                    (assert-equal? (get r 'message) "Holi")
                ]
            )
        """
        results = BotlangTester.run(self.bot_code, tests_code)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].is_failure())
        self.assertEqual(results[0].name, 'test-bot')
        self.assertTrue('Holi' in results[0].failed_assert.message)
        self.assertTrue('!=' in results[0].failed_assert.message)
        self.assertTrue('Bienvenido' in results[0].failed_assert.message)

        tests_code = """
            (define test-2
                [function (bot)
                    [define r (send-message bot "hola")]
                    (assert (starts-with? (get r 'message) "Holi"))
                ]
            )
        """
        results = BotlangTester.run(self.bot_code, tests_code)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].is_failure())
        self.assertEqual(results[0].name, 'test-2')
        self.assertEqual(
            results[0].failed_assert.message,
            'Expression evaluated to false'
        )

        tests_code = """
            (define test-miau
                [function (bot)
                    [define r (send-message bot "hola")]
                    (assert (starts-with? r "Holi"))
                ]
            )
        """
        results = BotlangTester.run(self.bot_code, tests_code)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].is_error())
        self.assertEqual(results[0].name, 'test-miau')
        self.assertTrue(
            results[0].error.message.__contains__(
                "requires a 'str' object but received a 'dict'"
            )
        )

    def test_results_to_dict(self):

        tests_code = """
            (define test-botcito
                [function (bot)
                    [define r2 (send-message bot "hola")]
                    (assert (starts-with? (get r2 'message) "Bienvenido a Botcenter!"))
                ]
            )
        """
        results = BotlangTester.run(self.bot_code, tests_code)
        self.assertEqual(len(results), 1)
        result_dict = results[0].to_dict()
        self.assertEqual(result_dict['result'], 'passed')
        self.assertEqual(result_dict['test_name'], 'test-botcito')

        tests_code = """
            (define test-bot
                [function (bot)
                    [define r (send-message bot "hola")]
                    (assert-equal? (get r 'message) "Holi")
                ]
            )
        """
        results = BotlangTester.run(self.bot_code, tests_code)
        self.assertEqual(len(results), 1)
        result_dict = results[0].to_dict()
        self.assertEqual(result_dict['result'], 'failed')
        self.assertEqual(result_dict['test_name'], 'test-bot')
        self.assertTrue('Holi' in result_dict['message'])
        self.assertTrue('!=' in result_dict['message'])
        self.assertTrue('Bienvenido' in result_dict['message'])

        tests_code = """
            (define test-miau
                [function (bot)
                    [define r (send-message bot "hola")]
                    (assert (starts-with? r "Holi"))
                ]
            )
        """
        results = BotlangTester.run(self.bot_code, tests_code)
        self.assertEqual(len(results), 1)
        result_dict = results[0].to_dict()
        self.assertEqual(result_dict['result'], 'error')
        self.assertEqual(result_dict['test_name'], 'test-miau')
        self.assertTrue(
            result_dict['message'].__contains__(
                "requires a 'str' object but received a 'dict'"
            )
        )

    def test_mocks(self):

        bot_code = """
            (bot-node (data)
                [define response (http-get "http://www.hola.chao")]
                (node-result
                    data
                    response
                    end-node
                )
            )
        """

        test_code = """
            [define mock-http-get
                (function (url)
                    "Hola"
                )
            ]
            [define test-bot
                (function (bot)
                    [define r (send-message bot "hola")]
                    (assert-equal? (get r 'message) "Hola")
                )
            ]
        """
        results = BotlangTester.run(bot_code, test_code)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].is_success())

    def test_input_data(self):

        bot_code = """
            (bot-node (data)
                (node-result
                    data
                    (append "Hi, " (get data 'name))
                    end-node
                )
            )
        """

        test_code = """
            [define input-data
                (make-dict '[(name "Pedro")])
            ]
            [define test-me
                (function (bot)
                    [define r (send-message bot "Holo")]
                    (assert-equal? (get r 'message) "Hi, Pedro")
                )
            ]
        """
        results = BotlangTester.run(bot_code, test_code)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].is_success())
