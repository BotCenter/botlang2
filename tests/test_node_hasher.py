import unittest

from botcenterdsl import Parser, Environment
from botcenterdsl.node_hasher import NodeHasher
from tests.example_bots import ExampleBots


class NodeHasherTestCase(unittest.TestCase):

    def test_node_hashing(self):

        ast = Parser.parse(ExampleBots.dog_bot_code)
        node_hasher = NodeHasher()
        ast.accept(node_hasher, Environment())
        bot_nodes = node_hasher.ast_nodes

        # self.assertEqual(len(bot_nodes.values()), 4)
