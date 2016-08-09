# -*- coding: utf-8 -*-
import unittest

from botcenterdsl.bot_configuration import BotConfiguration
from botcenterdsl.interpreter import BotcenterDSL


class TestBots(unittest.TestCase):

    example_bot_code = """
        (define ask-rut
            [function (data ask-rut-message next-node-fun)
                (define validate-rut-node
                    [bot-node (data)
                        (define rut input-message)
                        (define valid-rut? [validate-rut rut])
                        (if valid-rut?
                            (next-node-fun (add-data data 'rut rut))
                            (node-result
                                data
                                "Rut inválido. Intente nuevamente."
                                validate-rut-node
                            )
                        )
                    ]
                )
                (node-result
                    data
                    ask-rut-message
                    validate-rut-node
                )
            ]
        )

        (define has-dog-node
            (bot-node (data)
                (define valid-answer
                    [or (equal? input-message "si") (equal? input-message "no")]
                )
                (if (not valid-answer)
                    (node-result
                        data
                        "Debe responder si o no. ¿Tiene perro?"
                        has-dog-node
                    )
                    [if (equal? input-message "si")
                        (node-result
                            (add-data data 'dog #t)
                            "Wauf!"
                            end-node
                        )
                        (node-result
                            (add-data data 'dog #f)
                            "Miau :3"
                            end-node
                        )
                    ]
                )
            )
        )

        (bot-node (data)
            (node-result
                data
                "Bienvenido a Botcenter! ¿Con quién tengo el gusto de hablar?"
                (bot-node (data)
                    (define name input-message)
                    [ask-rut
                        (add-data data 'name name)
                        (append "Mucho gusto " name ". Indíqueme su RUT, por favor.")
                        (function (data)
                            (node-result
                                data
                                "Muchas gracias. ¿Tiene perro? (si/no)"
                                has-dog-node
                            )
                        )
                    ]
                )
            )
        )
    """

    def test_example_bot(self):

        def hook(node_result):
            if not node_result.next_node.is_bot_node():
                node_result.next_node()
            return node_result

        def validate_rut(rut):
            if rut == '16926695-6':
                return True
            return False

        test_dict = {'bot_ended': False}

        bot_config = BotConfiguration(
            result_hook=hook,
            functions={
                'validate-rut': validate_rut,
                'end-node': (lambda: test_dict.update(bot_ended=True))
            }
        )

        first_result = BotcenterDSL(bot_config=bot_config).eval(
            self.example_bot_code
        )

        self.assertEqual(
            first_result.message,
            'Bienvenido a Botcenter! ¿Con quién tengo el gusto de hablar?'
        )
        self.assertEqual(first_result.data, {})

        second_node = first_result.next_node
        second_result = BotcenterDSL(bot_config=bot_config).resume_execution(
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
        third_result = BotcenterDSL(bot_config=bot_config).resume_execution(
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
        fourth_result = BotcenterDSL(bot_config=bot_config).resume_execution(
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
        fifth_result = BotcenterDSL(bot_config=bot_config).resume_execution(
            fifth_node,
            fourth_result.data,
            'bla'
        )
        self.assertEqual(
            fifth_result.message,
            'Debe responder si o no. ¿Tiene perro?'
        )

        self.assertFalse(test_dict['bot_ended'])
        sixth_node = fifth_result.next_node
        sixth_result = BotcenterDSL(bot_config=bot_config).resume_execution(
            sixth_node,
            fifth_result.data,
            'no'
        )
        self.assertEqual(sixth_result.message, 'Miau :3')
        self.assertTrue(test_dict['bot_ended'])

        alternative_sixth_result = BotcenterDSL(
            bot_config=bot_config
        ).resume_execution(
            sixth_node,
            fifth_result.data,
            'si'
        )
        self.assertEqual(alternative_sixth_result.message, 'Wauf!')
