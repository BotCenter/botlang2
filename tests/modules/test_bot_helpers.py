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

    def test_format_simple_list(self):

        code = """
        (require "bot-helpers")
        (format-simple-list
            (make-dict (list))
            "Hola"
            (list
                (cons "Juanito" "Lechuga")
                (cons "Edulio" "Caluga")
            )
        )
        """
        result = BotlangSystem.bot_instance().eval_bot(code, input_msg='')
        self.assertEqual(
            result,
            'Hola\n\nJuanito. Lechuga\n\nEdulio. Caluga'
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
