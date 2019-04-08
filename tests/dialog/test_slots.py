from unittest import TestCase

from botlang import BotlangSystem


class SlotsTestCase(TestCase):

    SLOTS_EXAMPLE = """
    (defun default-behavior (c m)
        (cond
            [(match? "ctm" m)
                (node-result c "No me insultes" (return end-node))
            ]
            [(match? "chao" m) (node-result c "Adiós" end-node)]
            [else nil]
        )
    )

    (bot node2 (c m) (default-behavior c m))

    (slots-node node1 (c m)
        %s
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
                [(match? "si(\\s.*)?" m) #t]
                [(match? "no(\\s.*)?" m) #f]
                [else nil]
            )
            "¿Lo quieres con crema?"
        ]
        [then
            (node-result c
                (append
                    "Tu pedido es un " (get c "type") " " (get c "size") " "
                    (if (get c "with-cream") "con crema" "sin crema")
                )
                end-node
            )
        ]
    )
    """

    SLOTS_DIGRESS = SLOTS_EXAMPLE % '[digress (default-behavior c m)]'
    SLOTS_NO_DIGRESS = SLOTS_EXAMPLE % ''

    def test_answer_correctly(self):

        r1 = BotlangSystem().eval_bot(self.SLOTS_DIGRESS, 'hola')
        self.assertEqual(r1.message, '¿De qué tipo quieres tu café?')
        self.assertEqual(r1.next_node, 'node1')

        r2 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'latte', r1.next_node, r1.data
        )
        self.assertEqual(r2.message, '¿De qué tamaño quieres tu café?')
        self.assertEqual(r2.data.get('type'), 'latte')
        self.assertEqual(r2.next_node, 'node1')

        r3 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'mediano', r2.next_node, r2.data
        )
        self.assertEqual(r3.message, '¿Lo quieres con crema?')
        self.assertEqual(r3.data.get('size'), 'mediano')
        self.assertEqual(r3.next_node, 'node1')

        r4 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'no', r2.next_node, r2.data
        )
        self.assertEqual(r4.message, 'Tu pedido es un latte mediano sin crema')
        self.assertEqual(r4.data.get('with-cream'), False)
        self.assertEqual(r4.next_node, None)

    def test_give_partial_information(self):

        r1 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS,
            'Hola, quiero un cafe mocha grande por favor'
        )
        self.assertEqual(r1.message, '¿Lo quieres con crema?')
        self.assertEqual(r1.data.get('type'), 'mocha')
        self.assertEqual(r1.data.get('size'), 'grande')
        self.assertEqual(r1.next_node, 'node1')

        r2 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'si', r1.next_node, r1.data
        )
        self.assertEqual(r2.message, 'Tu pedido es un mocha grande con crema')
        self.assertEqual(r2.data.get('with-cream'), True)
        self.assertEqual(r2.next_node, None)

    def test_answer_incorrectly_no_digress(self):

        r1 = BotlangSystem().eval_bot(
            self.SLOTS_NO_DIGRESS,
            'Hola, quiero un cafe americano chico por favor'
        )
        self.assertEqual(r1.message, '¿Lo quieres con crema?')
        self.assertEqual(r1.next_node, 'node1')

        r2 = BotlangSystem().eval_bot(
            self.SLOTS_NO_DIGRESS, 'qwerty', r1.next_node, r1.data
        )
        self.assertEqual(r2.message, '¿Lo quieres con crema?')
        self.assertEqual(r2.next_node, 'node1')

        r3 = BotlangSystem().eval_bot(
            self.SLOTS_NO_DIGRESS, 'no', r2.next_node, r2.data
        )
        self.assertEqual(
            r3.message, 'Tu pedido es un americano chico sin crema'
        )
        self.assertEqual(r3.next_node, None)

    def test_digression(self):

        r1 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS,
            'Hola, quiero un latte por favor'
        )
        self.assertEqual(r1.message, '¿De qué tamaño quieres tu café?')
        self.assertEqual(r1.next_node, 'node1')

        # Digression with return
        r2 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'ctm', r1.next_node, r1.data
        )
        self.assertEqual(r2.message, 'No me insultes')
        self.assertEqual(r2.next_node, 'node1')

        r3 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'lo quiero mediano', r2.next_node, r2.data
        )
        self.assertEqual(r3.message, '¿Lo quieres con crema?')
        self.assertEqual(r3.next_node, 'node1')

        # Digression without return
        r4 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'chao', r3.next_node, r3.data
        )
        self.assertEqual(r4.message, 'Adiós')
        self.assertEqual(r4.next_node, None)
        self.assertEqual(r4.bot_state, 'BOT_ENDED')

    def test_return_does_not_interfere(self):

        r = BotlangSystem().eval_bot(self.SLOTS_DIGRESS, 'ctm', 'node2')
        self.assertEqual(r.message, 'No me insultes')
        self.assertEqual(r.next_node, None)
        self.assertEqual(r.bot_state, 'BOT_ENDED')
