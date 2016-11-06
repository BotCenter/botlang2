import unittest
from botlang.interpreter import BotlangSystem


class BotlangTestCase(unittest.TestCase):

    def test_filter(self):

        filtered_list = BotlangSystem.run("""
            (filter (function (v) (> v 3)) (list 5 2 8 9 1 33 -1 -5 4))
        """)
        self.assertEqual(filtered_list, [5, 8, 9, 33, 4])
