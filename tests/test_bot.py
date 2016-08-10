# -*- coding: utf-8 -*-
import unittest

from botcenterdsl.interpreter import BotcenterDSL
from tests.example_bots import ExampleBots


class TestBots(unittest.TestCase):

    def test_example_bot(self):

        def validate_rut(rut):
            if rut == '16926695-6':
                return True
            return False

        environment = BotcenterDSL.create_base_environment().add_primitives(
            {
                'validate-rut': validate_rut,
                'end-node': lambda: 'BOT_ENDED'
            }
        )

        first_result = BotcenterDSL(environment).eval_bot(
            ExampleBots.dog_bot_code
        )

        self.assertEqual(
            first_result.message,
            'Bienvenido a Botcenter! ¿Con quién tengo el gusto de hablar?'
        )
        self.assertEqual(first_result.data, {})

        second_node = first_result.next_node
        second_result = BotcenterDSL(environment).execute_from_node(
            second_node,
            first_result.data,
            'Juanito'
        )
        self.assertEqual(
            second_result.message,
            'Mucho gusto Juanito. Indíqueme su RUT, por favor.'
        )
        self.assertEqual(len(second_result.data.items()), 1)
        self.assertEqual(second_result.data.get('name'), 'Juanito')

        third_node = second_result.next_node
        third_result = BotcenterDSL(environment).execute_from_node(
            third_node,
            second_result.data,
            '17098131-2'
        )

        self.assertEqual(len(third_result.data.items()), 1)
        self.assertEqual(
            third_result.message,
            'Rut inválido. Intente nuevamente.'
        )

        fourth_node = third_result.next_node
        fourth_result = BotcenterDSL(environment).execute_from_node(
            fourth_node,
            third_result.data,
            '16926695-6'
        )

        self.assertEqual(len(fourth_result.data.items()), 2)
        self.assertEqual(fourth_result.data.get('rut'), '16926695-6')
        self.assertEqual(
            fourth_result.message,
            'Muchas gracias. ¿Tiene perro? (si/no)'
        )

        fifth_node = fourth_result.next_node
        fifth_result = BotcenterDSL(environment).execute_from_node(
            fifth_node,
            fourth_result.data,
            'bla'
        )
        self.assertEqual(
            fifth_result.message,
            'Debe responder si o no. ¿Tiene perro?'
        )

        self.assertEqual(fifth_result.execution_state, 'WAITING_INPUT')
        sixth_node = fifth_result.next_node
        sixth_result = BotcenterDSL(environment).execute_from_node(
            sixth_node,
            fifth_result.data,
            'no'
        )
        self.assertEqual(sixth_result.message, 'Miau :3')
        self.assertEqual(sixth_result.execution_state, 'BOT_ENDED')

        alternative_sixth_result = BotcenterDSL(environment).execute_from_node(
            sixth_node,
            fifth_result.data,
            'si'
        )
        self.assertEqual(alternative_sixth_result.message, 'Wauf!')
