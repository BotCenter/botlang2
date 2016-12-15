from unittest import TestCase

from botlang import BotlangSystem


class PlainFormatterTestCase(TestCase):

    def test_format_list(self):

        code = """
        (require "plain-formatter")
        (format-plain-simple-list
            "VITAL APOQUINDO ESQ. / VIA LACTEA"
            (list
                (cons "501: Menos de 5 min" "A 197 metros. Patente BJFD-87")
                (cons "C03: Menos de 5 min" "A 401 metros. Patente CJRT-77")
                (cons "518: Menos de 5 min" "A 406 metros. Patente BJFR-37")
                (cons "427: Menos de 5 min" "A 982 metros. Patente CJRS-49")
            )
        )
        """
        result = BotlangSystem.bot_instance().eval_bot(code, '')
        self.assertEqual(
            result,
            'VITAL APOQUINDO ESQ. / VIA LACTEA'
            '\n\n501: Menos de 5 min. A 197 metros. Patente BJFD-87\n\nC03: '
            'Menos de 5 min. A 401 metros. Patente CJRT-77\n\n518: Menos de 5 '
            'min. A 406 metros. Patente BJFR-37\n\n427: Menos de 5 min. A 982 '
            'metros. Patente CJRS-49'
        )
