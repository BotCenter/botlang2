from unittest import TestCase
from urllib.parse import quote

from botlang import BotlangSystem


class HttpTestCase(TestCase):

    def test_uri_escape(self):

        test_segment = "Pascual Baburizza 595"
        unescaped = BotlangSystem.run('"%s"' % test_segment)
        escaped = BotlangSystem.run('(uri-escape "%s")' % test_segment)
        expected = quote(test_segment)

        self.assertNotEqual(unescaped, expected)
        self.assertEqual(escaped, expected)
