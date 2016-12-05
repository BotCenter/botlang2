from unittest import TestCase

from botlang import BotlangSystem


class BotHelpersTestCase(TestCase):

    def test_validate_rut(self):

        dsl = BotlangSystem.bot_instance()

        self.assertTrue(
            dsl.eval('(require "bot-helpers") (validate-rut "16926695-6")')
        )
        self.assertTrue(
            dsl.eval('(require "bot-helpers") (validate-rut "16.926.695-6 ")')
        )
        self.assertTrue(
            dsl.eval('(require "bot-helpers") (validate-rut " 30.686.957-4")')
        )
        self.assertTrue(
            dsl.eval('(require "bot-helpers") (validate-rut "7015383-1")')
        )
        self.assertFalse(
            dsl.eval('(require "bot-helpers") (validate-rut "16926695-5")')
        )
        self.assertFalse(
            dsl.eval('(require "bot-helpers") (validate-rut "16.926.696-6")')
        )
        self.assertFalse(
            dsl.eval('(require "bot-helpers") (validate-rut "30.685.957-4")')
        )
        self.assertFalse(
            dsl.eval('(require "bot-helpers") (validate-rut "7015383-0")')
        )
        self.assertFalse(
            dsl.eval('(require "bot-helpers") (validate-rut "70153830")')
        )

    def test_ask_with_retries(self):

        code = """
        (require "bot-helpers")

        [define exit-node
            (function (message)
                (bot-node (data)
                    (node-result
                        data
                        message
                        end-node
                    )
                )
            )
        ]
        [define success-node (exit-node "Gracias :)")]
        [define invalid-rut-exit-node (exit-node "Rut inválido. Adiós.")]

        (bot-node (data)
            (ask-with-retries
                data
                "Hola"
                validate-rut
                'rut
                success-node
                2
                "Rut inválido. Intente nuevamente."
                invalid-rut-exit-node
            )
        )
        """
        r = BotlangSystem.bot_instance().eval_bot(code, input_msg='hola')
        self.assertEqual(r.message, 'Hola')
        state = r.execution_state
        self.assertEqual(state.bot_node_steps, 1)

        r = BotlangSystem.bot_instance().eval_bot(
            code, input_msg='1515151-1', evaluation_state=state
        )
        state = r.execution_state
        self.assertEqual(state.bot_node_steps, 2)
        self.assertEqual(r.message, u'Rut inválido. Intente nuevamente.')

