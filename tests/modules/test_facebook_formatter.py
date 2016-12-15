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

    def test_format_list(self):

        code = """
        (require "facebook-formatter")
        (format-facebook-simple-list
            "VITAL APOQUINDO ESQ. / VIA LACTEA"
            (list
                (cons "501: Menos de 5 min" "A 197 metros. Patente BJFD-87")
                (cons "C03: Menos de 5 min" "A 401 metros. Patente CJRT-77")
                (cons "518: Menos de 5 min" "A 406 metros. Patente BJFR-37")
                (cons "427: Menos de 5 min" "A 982 metros. Patente CJRS-49")
                (cons "427: Menos de 5 min" "A 982 metros. Patente CJRS-49")
            )
        )
        """
        result = BotlangSystem.bot_instance().eval_bot(code, '')
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], 'VITAL APOQUINDO ESQ. / VIA LACTEA')
        self.assertDictEqual(
            result[1],
            {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'list',
                        'top_element_style': 'compact',
                        'elements': [
                            {
                                'title': '501: Menos de 5 min',
                                'subtitle': 'A 197 metros. Patente BJFD-87'
                            },
                            {
                                'title': 'C03: Menos de 5 min',
                                'subtitle': 'A 401 metros. Patente CJRT-77'
                            },
                            {
                                'title': '518: Menos de 5 min',
                                'subtitle': 'A 406 metros. Patente BJFR-37'
                            }
                        ]
                    }
                }
            }
        )
        self.assertDictEqual(
            result[2],
            {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'list',
                        'top_element_style': 'compact',
                        'elements': [
                            {
                                'title': '427: Menos de 5 min',
                                'subtitle': 'A 982 metros. Patente CJRS-49'
                            },
                            {
                                'title': '427: Menos de 5 min',
                                'subtitle': 'A 982 metros. Patente CJRS-49'
                            }
                        ]
                    }
                }
            }
        )

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
