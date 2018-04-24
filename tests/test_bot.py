# -*- coding: utf-8 -*-
import unittest

from botlang.examples.example_bots import ExampleBots
from botlang.interpreter import BotlangSystem


class TestBots(unittest.TestCase):

    def test_input_data(self):

        code = """
            (bot-node (data)
                (node-result
                    (put data 'bla "da")
                    "Hi"
                    end-node
                )
            )
        """
        input_data = {'some-data': 'hola', 'more-data': 'chao'}
        result = BotlangSystem.bot_instance().eval_bot(
            code,
            'Hola',
            data=input_data
        )
        self.assertDictEqual(
            result.data,
            {'some-data': 'hola', 'more-data': 'chao', 'bla': 'da'}
        )

    def test_dict_messages(self):

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
        result = BotlangSystem.bot_instance().eval_bot(
            code,
            {'message': 'Hola'}
        )
        self.assertDictEqual(
            result.message,
            {'answer': 'Hola'}
        )

    def test_example_bot(self):

        code = ExampleBots.bank_bot_code

        first_result = BotlangSystem.bot_instance().eval_bot(code, 'hola')
        self.assertEqual(
            first_result.message[0],
            'ENTRY_MESSAGE'
        )
        self.assertSequenceEqual(first_result.data.get('nodes-path'), [])
        self.assertEqual(first_result.bot_state, 'WAITING_INPUT')

        second_result = BotlangSystem.bot_instance().eval_bot(
            code,
            'tengo una emergencia',
            first_result.next_node,
            first_result.data
        )
        self.assertEqual(
            second_result.message[0],
            'EMERGENCIAS_CABECERA'
        )
        self.assertEqual(len(second_result.data.items()), 2)
        self.assertSequenceEqual(
            second_result.data.get('nodes-path'),
            ['EMERGENCIA']
        )
        self.assertEqual(second_result.bot_state, 'WAITING_INPUT')

        third_result = BotlangSystem.bot_instance().eval_bot(
            code,
            'tuve un problema con mi auto',
            second_result.next_node,
            second_result.data
        )
        self.assertSequenceEqual(
            third_result.data.get('nodes-path'),
            ['EMERGENCIA', 'AUTO']
        )
        self.assertEqual(
            third_result.message[0],
            'SIGUIENTES_PASOS'
        )
        self.assertEqual(third_result.bot_state, 'WAITING_INPUT')

        fourth_result = BotlangSystem.bot_instance().eval_bot(
            code,
            'No',
            third_result.next_node,
            third_result.data
        )
        self.assertEqual(
            fourth_result.message['text'],
            'TE_SIRVIO?'
        )
        self.assertEqual(fourth_result.bot_state, 'WAITING_INPUT')

        fifth_result = BotlangSystem.bot_instance().eval_bot(
            code,
            'Si',
            fourth_result.next_node,
            fourth_result.data
        )
        self.assertEqual(
            fifth_result.message[0],
            'DESPEDIDA'
        )
        self.assertEqual(fifth_result.bot_state, 'CLOSE_TICKET')

    def test_bot_recursion(self):

        code = """
            [define get-count
                (function (data)
                    [define c (get-or-nil data "counter")]
                    (if (nil? c) 0 c)
                )
            ]
            [define node1
                (bot-node (data)
                    [define count (+ (get-count data) 1)]
                    (node-result
                        (put data "counter" count)
                        count
                        node1
                    )
                )
            ]
            node1
        """
        r1 = BotlangSystem.bot_instance().eval_bot(code, '')
        self.assertEqual(r1.message, 1)

        r2 = BotlangSystem.bot_instance().eval_bot(
            code, '', r1.next_node, r1.data
        )
        self.assertEqual(r2.message, 2)

        r3 = BotlangSystem.bot_instance().eval_bot(
            code, '', r2.next_node, r2.data
        )
        self.assertEqual(r3.message, 3)

        r = r3
        for i in range(0, 10):
            r = BotlangSystem.bot_instance().eval_bot(
                code, '', r.next_node, r.data
            )

        self.assertEqual(r.message, 13)
