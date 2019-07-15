from unittest import TestCase

from botlang import BotlangSystem


class SlotsTestCase(TestCase):

    SLOTS_EXAMPLE = """
    (defun default-behavior (c m)
        (cond
            [(match? "ctm" m)
                (node-result c "No me insultes" (return end-node))
            ]
            [(match? "digress?" m)
                (node-result c (if (digression?) "Sí" "No") (return end-node))
            ]
            [(match? "chao" m) (node-result c "Adiós" end-node)]
            [(match? "coffee" m) (node1 (reset-context c) m)]
            [else nil]
        )
    )
    
    (defun reset-context (c)
        (begin
            (remove! c "type")
            (remove! c "size")
            (remove! c "with-cream")
            (remove! c "confirm")
        )
    )
    
    (slots-node node3 (c m)
        [slot confirm c
            (cond
                [(match? "si" m) #t]
                [(match? "no" m) #f]
                [else nil]
            )
            "¿Confirmas tu pedido?"
        ]
        [then (if (get c "confirm")
            (node-result c
                (if (get-or-nil c "discount")
                    "Confirmado. Te saldrá gratis :)"
                    "Confirmado"
                )
                end-node
            )
            (node-result
                (reset-context c)
                "Bueno, ¿qué café quieres?"
                node1
            )
        )]
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
        [slot discount c (match "descuento\\s(\\d+)" m 1)]
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
                    (if (get c "with-cream") "con crema?" "sin crema?")
                )
                node3
            )
        ]
    )
    """

    SLOTS_DIGRESS = SLOTS_EXAMPLE % '[digress (default-behavior c m)]'
    SLOTS_NO_DIGRESS = SLOTS_EXAMPLE % ''
    SLOTS_WITH_BEFORE = SLOTS_EXAMPLE % '[before (if (equal? "a" m)' \
                                        ' (put! c "meta" "a")' \
                                        ' (put! c "meta" "b"))]'

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
            self.SLOTS_DIGRESS, 'no', r3.next_node, r3.data
        )
        self.assertEqual(r4.message, 'Tu pedido es un latte mediano sin crema?')
        self.assertEqual(r4.data.get('with-cream'), False)
        self.assertEqual(r4.next_node, 'node3')

        r5 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'si', r4.next_node, r4.data
        )
        self.assertEqual(r5.message, 'Confirmado')
        self.assertEqual(r5.data.get('confirm'), True)
        self.assertEqual(r5.next_node, None)

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
        self.assertEqual(r2.message, 'Tu pedido es un mocha grande con crema?')
        self.assertEqual(r2.data.get('with-cream'), True)
        self.assertEqual(r2.next_node, 'node3')

        r3 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'no', r2.next_node, r2.data
        )
        self.assertEqual(r3.message, 'Bueno, ¿qué café quieres?')
        self.assertEqual(r3.next_node, 'node1')

        r4 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'un latte grande', r3.next_node, r3.data
        )
        self.assertEqual(r4.message, '¿Lo quieres con crema?')
        self.assertEqual(r4.next_node, 'node1')

        r5 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'si', r4.next_node, r4.data
        )
        self.assertEqual(r5.message, 'Tu pedido es un latte grande con crema?')
        self.assertEqual(r5.next_node, 'node3')

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
            r3.message, 'Tu pedido es un americano chico sin crema?'
        )
        self.assertEqual(r3.next_node, 'node3')

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

    def test_before_block(self):

        r = BotlangSystem().eval_bot(self.SLOTS_WITH_BEFORE, 'hola', 'node1')
        self.assertEqual(r.data['meta'], 'b')

        r = BotlangSystem().eval_bot(self.SLOTS_WITH_BEFORE, 'a', 'node1')
        self.assertEqual(r.data['meta'], 'a')

    def test_recursive_digression(self):

        r1 = BotlangSystem().eval_bot(self.SLOTS_DIGRESS, 'mocha', 'node1')
        self.assertEqual(r1.message, '¿De qué tamaño quieres tu café?')
        self.assertEqual(r1.next_node, 'node1')

        r2 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'coffee', r1.next_node, r1.data
        )
        self.assertEqual(r2.message, '¿De qué tipo quieres tu café?')
        self.assertEqual(r2.next_node, 'node1')

    def test_in_disgression_check(self):

        r1 = BotlangSystem().eval_bot(self.SLOTS_DIGRESS, 'digress?', 'node1')
        self.assertEqual(r1.message, 'Sí')

        r2 = BotlangSystem().eval_bot(self.SLOTS_DIGRESS, 'digress?', 'node2')
        self.assertEqual(r2.message, 'No')

    def test_optional_slot(self):

        r1 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'descuento 123 para mocha chico', 'node1'
        )
        self.assertEqual(r1.data.get('discount'), '123')
        self.assertEqual(r1.message, '¿Lo quieres con crema?')

        r2 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'si', r1.next_node, r1.data
        )
        self.assertEqual(r2.message, 'Tu pedido es un mocha chico con crema?')

        r3 = BotlangSystem().eval_bot(
            self.SLOTS_DIGRESS, 'si', r2.next_node, r2.data
        )
        self.assertEqual(r3.message, 'Confirmado. Te saldrá gratis :)')
