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
        code = ExampleBots.dog_bot_code

        first_result = BotcenterDSL(environment).eval_bot(code, 'hola')
        self.assertEqual(
            first_result.message,
            'Bienvenido a Botcenter! ¿Con quién tengo el gusto de hablar?'
        )
        self.assertEqual(first_result.data, {})

        first_evaluation_state = first_result.evaluation_state
        second_result = BotcenterDSL(environment).eval_bot(
            code,
            'Juanito',
            first_evaluation_state
        )
        self.assertEqual(
            second_result.message,
            'Mucho gusto Juanito. Indíqueme su RUT, por favor.'
        )
        self.assertEqual(len(second_result.data.items()), 1)
        self.assertEqual(second_result.data.get('name'), 'Juanito')

        second_evaluation_state = second_result.evaluation_state
        third_result = BotcenterDSL(environment).eval_bot(
            code,
            '17098131-2',
            second_evaluation_state
        )

        self.assertEqual(len(third_result.data.items()), 1)
        self.assertEqual(
            third_result.message,
            'Rut inválido. Intente nuevamente.'
        )

        third_evaluation_state = third_result.evaluation_state
        fourth_result = BotcenterDSL(environment).eval_bot(
            code,
            '16926695-6',
            third_evaluation_state
        )

        self.assertEqual(len(fourth_result.data.items()), 2)
        self.assertEqual(fourth_result.data.get('rut'), '16926695-6')
        self.assertEqual(
            fourth_result.message,
            'Muchas gracias. ¿Tiene perro? (si/no)'
        )

        fourth_evaluation_state = fourth_result.evaluation_state
        self.assertEqual(fourth_evaluation_state.bot_node_steps, 4)
        fifth_result = BotcenterDSL(environment).eval_bot(
            code,
            'bla',
            fourth_evaluation_state
        )
        self.assertEqual(
            fifth_result.message,
            'Debe responder si o no. ¿Tiene perro?'
        )

        self.assertEqual(fifth_result.execution_state, 'WAITING_INPUT')

        fifth_evaluation_state = fifth_result.evaluation_state
        self.assertEqual(fifth_evaluation_state.bot_node_steps, 5)
        sixth_result = BotcenterDSL(environment).eval_bot(
            code,
            'no',
            fifth_evaluation_state
        )
        self.assertEqual(sixth_result.message, 'Miau :3')
        self.assertEqual(sixth_result.execution_state, 'BOT_ENDED')

        alternative_sixth_result = BotcenterDSL(environment).eval_bot(
            code,
            'si',
            fifth_evaluation_state
        )
        self.assertEqual(alternative_sixth_result.message, 'Wauf!')
