from collections import OrderedDict
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

    def test_node_selection(self):

        code = """
        (require "bot-helpers")

        [define node-1
            (bot-node (data)
                (node-result data "Node 1" end-node)
            )
        ]
        [define node-2
            (bot-node (data)
                (node-result data "Node 2" end-node)
            )
        ]
        [define node-3
            (bot-node (data)
                (node-result data "Node 3" end-node)
            )
        ]

        (bot-node (data)
            (node-selection
                data
                "Holi"
                (list
                    (option 1 "opcion 1" node-1)
                    (option 2 "opcion 2" node-2)
                    (option 3 "opcion 3" node-3)
                )
            )
        )
        """
        plain = BotlangSystem.bot_instance().eval_bot(code, input_msg='hola')
        state = plain.execution_state
        self.assertTrue("1) opcion 1" in plain.message)

        plain = BotlangSystem.bot_instance().eval_bot(
            code,
            input_msg="2",
            evaluation_state=state
        )
        self.assertEqual(plain.message, 'Node 2')

        fb = BotlangSystem.bot_instance().eval_bot(
            code,
            input_msg='bla',
            data={'social_network': 'facebook'}
        )
        self.assertDictEqual(
            fb.message,
            {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'button',
                        'text': 'Holi',
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'opcion 1',
                                'payload': 1
                            },
                            {
                                'type': 'postback',
                                'title': 'opcion 2',
                                'payload': 2
                            },
                            {
                                'type': 'postback',
                                'title': 'opcion 3',
                                'payload': 3
                            }
                        ]
                    }
                }
            }
        )

    def test_format_link(self):
        code = """
                (require "bot-helpers")

                (bot-node (data)
                    (node-result
                        data
                        (format-link-with-image
                            data
                            "Título"
                            "http://test.botlang.cl"
                            "http://test.botlang.cl/image.png"
                        )
                        end-node
                    )
                )
                """
        plain = BotlangSystem.bot_instance().eval_bot(code, input_msg='hi')
        self.assertTrue('Título:' in plain.message)
        self.assertTrue('http://test.botlang.cl' in plain.message)
        self.assertFalse('http://test.botlang.cl/image.png' in plain.message)

        fb = BotlangSystem.bot_instance().eval_bot(
            code,
            input_msg='hi',
            data={'social_network': 'facebook'}
        )
        self.assertDictEqual(
            fb.message,
            {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'generic',
                        'elements': [
                            {
                                'title': 'Título',
                                'item_url': 'http://test.botlang.cl',
                                'image_url': 'http://test.botlang.cl/image.png'
                            }
                        ]
                    }
                }
            }
        )
