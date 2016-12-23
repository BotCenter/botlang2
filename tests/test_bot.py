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

        code = ExampleBots.dog_bot_code

        first_result = BotlangSystem.bot_instance().eval_bot(code, 'hola')
        self.assertEqual(
            first_result.message,
            'Bienvenido a Botcenter! ¿Con quién tengo el gusto de hablar?'
        )
        self.assertEqual(first_result.data, {})

        first_execution_state = first_result.execution_state
        second_result = BotlangSystem.bot_instance().eval_bot(
            code,
            'Juanito',
            first_execution_state
        )
        self.assertEqual(
            second_result.message,
            'Mucho gusto Juanito. Indíqueme su RUT, por favor.'
        )
        self.assertEqual(len(second_result.data.items()), 1)
        self.assertEqual(second_result.data.get('name'), 'Juanito')

        second_execution_state = second_result.execution_state
        third_result = BotlangSystem.bot_instance().eval_bot(
            code,
            '17098131-2',
            second_execution_state
        )

        self.assertEqual(len(third_result.data.items()), 1)
        self.assertEqual(
            third_result.message,
            'Rut inválido. Intente nuevamente.'
        )

        third_execution_state = third_result.execution_state
        fourth_result = BotlangSystem.bot_instance().eval_bot(
            code,
            '16926695-6',
            third_execution_state
        )

        self.assertEqual(len(fourth_result.data.items()), 2)
        self.assertEqual(fourth_result.data.get('rut'), '16926695-6')
        self.assertEqual(
            fourth_result.message,
            'Muchas gracias. ¿Tiene perro? (si/no)'
        )

        fourth_execution_state = fourth_result.execution_state
        self.assertEqual(fourth_execution_state.bot_node_steps, 4)
        fifth_result = BotlangSystem.bot_instance().eval_bot(
            code,
            'bla',
            fourth_execution_state
        )
        self.assertEqual(
            fifth_result.message,
            'Debe responder si o no. ¿Tiene perro?'
        )

        self.assertEqual(fifth_result.bot_state, 'WAITING_INPUT')

        fifth_execution_state = fifth_result.execution_state
        self.assertEqual(fifth_execution_state.bot_node_steps, 5)
        sixth_result = BotlangSystem.bot_instance().eval_bot(
            code,
            'no',
            fifth_execution_state
        )
        self.assertEqual(sixth_result.message, 'Miau, Juanito :3')
        self.assertEqual(sixth_result.bot_state, 'BOT_ENDED')

        alternative_sixth_result = BotlangSystem.bot_instance().eval_bot(
            code,
            'si',
            fifth_execution_state
        )
        self.assertEqual(alternative_sixth_result.message, 'Wauf, "Juanito"!')

    def test_primitives_caching(self):

        environment = BotlangSystem.base_environment()
        code = """
        [define node-two
            (bot-node (data)
                [define washo
                    (append [input-message] "\n" (get data 'mensajito))
                ]
                (node-result
                    (put data 'washo washo)
                    washo
                    end-node
                )
            )
        ]
        [define some-list (list 1 2 3 4)]
        [define concatenate
            (fun (list)
                [reduce
                    (fun (acc next) [append (str acc) "\n" (str next)])
                    list
                ]
            )
        ]

        (bot-node (data)
            (node-result
                (put data 'mensajito [concatenate some-list])
                "Hola"
                node-two
            )
        )
        """
        first_result = BotlangSystem(environment).eval_bot(code, 'hola')
        self.assertEqual(
            first_result.message,
            'Hola'
        )
        self.assertEqual(
            first_result.data,
            {'mensajito': '1\n2\n3\n4'}
        )

        first_execution_state = first_result.execution_state
        second_result = BotlangSystem(environment).eval_bot(
            code,
            'Miau',
            first_execution_state
        )
        self.assertEqual(
            second_result.message,
            'Miau\n1\n2\n3\n4'
        )
