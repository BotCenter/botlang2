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
