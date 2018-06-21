import unittest

from botlang import BotlangErrorException
from botlang.interpreter import BotlangSystem


class BotlangTestCase(unittest.TestCase):

    def test_get_node(self):

        bot_code = """
        (define node1 (bot-node (context)
            (node-result
                context
                "Nodo 1"
                end-node
            )
        ))
        (define node2 1)
        (bot-node (context)
            ((get-node (input-message)) context)
        )
        """

        result = BotlangSystem.bot_instance().eval_bot(bot_code, 'node1')
        self.assertEqual(result.message, 'Nodo 1')

        with self.assertRaises(BotlangErrorException) as cm:
            BotlangSystem.bot_instance().eval_bot(bot_code, 'node3')
        self.assertTrue("name 'node3' is not defined" in str(cm.exception))

        with self.assertRaises(BotlangErrorException) as cm:
            BotlangSystem.bot_instance().eval_bot(bot_code, 'node2')
        self.assertTrue("'node2' is not a bot node" in str(cm.exception))
