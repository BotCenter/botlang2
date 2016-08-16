import unittest

from botcenterdsl import Parser, Environment
from botcenterdsl.examples.example_bots import ExampleBots
from botcenterdsl.node_hasher import NodeHasher


class RuntimeStateSerializationTestCase(unittest.TestCase):

    def test_deterministic_node_hashing(self):

        ast = Parser.parse(ExampleBots.dog_bot_code)
        node_hasher1 = NodeHasher()
        node_hasher2 = NodeHasher()

        ast.accept(node_hasher1, Environment())
        bot_nodes1 = node_hasher1.ast_nodes

        ast.accept(node_hasher2, Environment())
        bot_nodes2 = node_hasher2.ast_nodes

        self.assertDictEqual(bot_nodes1, bot_nodes2)
