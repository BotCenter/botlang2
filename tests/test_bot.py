# -*- coding: utf-8 -*-
import unittest

from botcenterdsl.examples.example_bots import ExampleBots
from botcenterdsl.interpreter import BotcenterDSL


class TestBots(unittest.TestCase):

    def test_example_bot(self):

        def validate_rut(rut):
            if rut == '16926695-6':
                return True
            return False

        environment = BotcenterDSL.base_environment().add_primitives(
            {
                'validate-rut': validate_rut,
                'end-node': lambda: 'BOT_ENDED'
            }
        )
        code = ExampleBots.dog_bot_code

        first_result = BotcenterDSL(environment).eval_bot(code, 'hola')
        self.assertEqual(
            first_result.message,
            'Bienvenido a Botcenter! ¿Con quién tengo el gusto de hablar?'
        )
        self.assertEqual(first_result.data, {})

        first_execution_state = first_result.execution_state
        second_result = BotcenterDSL(environment).eval_bot(
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
        third_result = BotcenterDSL(environment).eval_bot(
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
        fourth_result = BotcenterDSL(environment).eval_bot(
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
        fifth_result = BotcenterDSL(environment).eval_bot(
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
        sixth_result = BotcenterDSL(environment).eval_bot(
            code,
            'no',
            fifth_execution_state
        )
        self.assertEqual(sixth_result.message, 'Miau, Juanito :3')
        self.assertEqual(sixth_result.bot_state, 'BOT_ENDED')

        alternative_sixth_result = BotcenterDSL(environment).eval_bot(
            code,
            'si',
            fifth_execution_state
        )
        self.assertEqual(alternative_sixth_result.message, 'Wauf, Juanito!')

    def test_primitives_caching(self):

        environment = BotcenterDSL.base_environment().add_primitives(
            {'end-node': lambda: 'BOT_ENDED'}
        )
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
        first_result = BotcenterDSL(environment).eval_bot(code, 'hola')
        self.assertEqual(
            first_result.message,
            'Hola'
        )
        self.assertEqual(
            first_result.data,
            {'mensajito': '1\n2\n3\n4'}
        )

        first_execution_state = first_result.execution_state
        second_result = BotcenterDSL(environment).eval_bot(
            code,
            'Miau',
            first_execution_state
        )
        self.assertEqual(
            second_result.message,
            'Miau\n1\n2\n3\n4'
        )
