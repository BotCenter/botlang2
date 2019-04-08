from unittest import TestCase

from botlang import Parser
from botlang.ast import BotSlotsNode, SlotsNodeBody, App, SlotDefinition, \
    BotResult


class SlotsParsingTestCase(TestCase):

    def test_slots_sexpr(self):

        code = """
        (slots-node node1 (c m)
            [digress (default-behavior c m)]
            [slot type c
                (match ".*(americano|latte|mocha).*" m 1)
                "¿De qué tipo quieres tu café?"
            ]
            [slot size c
                (match ".*(chico|mediano|grande).*" m 1)
                "¿De qué tamaño quieres tu café?"
            ]
            [slot with-cream c
                (cond
                    [(match? "si" m) #t]
                    [(match? "no" m) #f]
                    [else nil]
                )
                "¿Lo quieres con crema?"
            ]
            [then
                (node-result c "Ok" end-node)
            ]
        )
        """
        slots_node = Parser.parse(code)[0]
        self.assertTrue(isinstance(slots_node, BotSlotsNode))
        self.assertEqual(slots_node.node_name, 'node1')
        self.assertSequenceEqual(slots_node.params, ['c', 'm'])
        self.assertTrue(isinstance(slots_node.body, SlotsNodeBody))

        body = slots_node.body
        self.assertSequenceEqual(body.params, ['c', 'm'])
        self.assertTrue(isinstance(body.digress, App))
        self.assertTrue(isinstance(body.then, BotResult))

        for slot in body.slots:
            self.assertTrue(isinstance(slot, SlotDefinition))

    def test_slots_without_digress(self):

        code = """
        (slots-node node2 (c m)
            [slot type c
                (match ".*(americano|latte|mocha).*" m 1)
                "¿De qué tipo quieres tu café?"
            ]
            [slot size c
                (match ".*(chico|mediano|grande).*" m 1)
                "¿De qué tamaño quieres tu café?"
            ]
            [slot with-cream c
                (cond
                    [(match? "si" m) #t]
                    [(match? "no" m) #f]
                    [else nil]
                )
                "¿Lo quieres con crema?"
            ]
            [then
                (node-result c "Ok" end-node)
            ]
        )
        """
        slots_node = Parser.parse(code)[0]
        self.assertTrue(isinstance(slots_node, BotSlotsNode))
        self.assertEqual(slots_node.node_name, 'node2')
        self.assertSequenceEqual(slots_node.params, ['c', 'm'])
        self.assertTrue(isinstance(slots_node.body, SlotsNodeBody))

        body = slots_node.body
        self.assertSequenceEqual(body.params, ['c', 'm'])
        self.assertIsNone(body.digress)
        self.assertTrue(isinstance(body.then, BotResult))

        for slot in body.slots:
            self.assertTrue(isinstance(slot, SlotDefinition))
