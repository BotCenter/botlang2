from unittest import TestCase

from botlang import BotlangSystem


class FacebookFormatterTestCase(TestCase):

    def test_separate_list(self):

        code = """
        (require "facebook-formatter")

        (separate-list
            (list 1 2 3 4 5 6 7 8)
            3
        )
        """
        result = BotlangSystem.bot_instance().eval(code)
        self.assertEqual([[1, 2, 3], [4, 5, 6], [7, 8]], result)

    def test_format_options(self):

        code = """
        (require "facebook-formatter")

        (bot-node (data)
            (node-result
                data
                (format-facebook-options
                    "Opciones"
                    (list
                        (cons 1 "option 1")
                        (cons 2 "option 2")
                        (cons 3 "option 3")
                        (cons 4 "option 4")
                        (cons 5 "option 5")
                    )
                )
                end-node
            )
        )
        """
        fb = BotlangSystem.bot_instance().eval_bot(
            code,
            input_msg='hi',
            data={'social_network': 'facebook'}
        )
        self.assertEqual(len(fb.message), 2)
        self.assertDictEqual(
            fb.message[0],
            {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'button',
                        'text': 'Opciones',
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'option 1',
                                'payload': 1
                            },
                            {
                                'type': 'postback',
                                'title': 'option 2',
                                'payload': 2
                            },
                            {
                                'type': 'postback',
                                'title': 'option 3',
                                'payload': 3
                            }
                        ]
                    }
                }
            }
        )
        self.assertDictEqual(
            fb.message[1],
            {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'button',
                        'text': u'\u2063',
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'option 4',
                                'payload': 4
                            },
                            {
                                'type': 'postback',
                                'title': 'option 5',
                                'payload': 5
                            }
                        ]
                    }
                }
            }
        )
