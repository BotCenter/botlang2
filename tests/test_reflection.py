import unittest

from botlang import BotlangErrorException
from botlang.evaluation.values import FunVal
from botlang.interpreter import BotlangSystem


class BotlangTestCase(unittest.TestCase):

    def test_get_value(self):

        bot_code = """
        (define val1 1)
        (define val2 "hola")
        (define val3 (fun (x) x))
        (bot-node (ctx msg)
            (node-result ctx (reflect-get msg) end-node)
        )
        """
        result = BotlangSystem.bot_instance().eval_bot(bot_code, 'val1')
        self.assertEqual(result.message, 1)

        result = BotlangSystem.bot_instance().eval_bot(bot_code, 'val2')
        self.assertEqual(result.message, 'hola')

        result = BotlangSystem.bot_instance().eval_bot(bot_code, 'val3')
        self.assertTrue(isinstance(result.message, FunVal))

        with self.assertRaises(BotlangErrorException) as cm:
            BotlangSystem.bot_instance().eval_bot(bot_code, 'val4')
        self.assertTrue("name 'val4' is not defined" in str(cm.exception))

    def test_get_function(self):

        bot_code = """
        (define fun1 (function (x) (* x x)))
        (define fun2 4)
        (bot-node (context message)
            (node-result
                context
                ((reflect-get-fun message) 3)
                end-node
            )
        )
        """
        result = BotlangSystem.bot_instance().eval_bot(bot_code, 'fun1')
        self.assertEqual(result.message, 9)

        with self.assertRaises(BotlangErrorException) as cm:
            BotlangSystem.bot_instance().eval_bot(bot_code, 'fun3')
        self.assertTrue("name 'fun3' is not defined" in str(cm.exception))

        with self.assertRaises(BotlangErrorException) as cm:
            BotlangSystem.bot_instance().eval_bot(bot_code, 'fun2')
        self.assertTrue("'fun2' is not a function" in str(cm.exception))

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
            ((reflect-get-node (input-message)) context)
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
