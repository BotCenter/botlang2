from unittest import TestCase

from botlang.environment.bot_helpers import *


class BotHelpersTestCase(TestCase):

    def test_validate_rut(self):

        self.assertTrue(validate_rut('16926695-6'))
        self.assertTrue(validate_rut('16.926.695-6 '))
        self.assertTrue(validate_rut(' 30.686.957-4'))
        self.assertTrue(validate_rut('7015383-1'))

        self.assertFalse(validate_rut('16926695-5'))
        self.assertFalse(validate_rut('16.926.696-6'))
        self.assertFalse(validate_rut('30.685.957-4'))
        self.assertFalse(validate_rut('7015383-0'))
