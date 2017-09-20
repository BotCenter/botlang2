import unittest

from botlang import Parser


class ASTTestCase(unittest.TestCase):

    def test_copy(self):

        original_ast = Parser.parse("""
        (begin
            [define entry-node
                (bot-node (input-data)
                    [define message (input-message)]
                    [define first-name [get (split (get input-data "name")) 0]]
                    [define data (put input-data "first-name" first-name)]
                    (cond
                        [(match? "SUCURSAL_.+" message)
                            (node-result data (sucursal-info message) end-node)
                        ]
                        [else
                            (entry-section data  (append "Hola " first-name))
                        ]
                    )
                )
            ]
            (bot-node (data)
                [define msg (input-message)]
                (if (equal? msg "")
                    (node-result data "" end-node)
                    (entry-node data)
                )
            )
        )
        """, source_id='test')[0]

        ast_copy = original_ast.copy()
        entry_node_body_copy = ast_copy.expressions[0].expr.body
        entry_node_body_copy.expressions[0].name = 'mensajito'

        entry_node_body_original = original_ast.expressions[0].expr.body
        self.assertEqual(
            entry_node_body_original.expressions[0].name,
            'message'
        )
        self.assertEqual(
            entry_node_body_copy.expressions[0].name,
            'mensajito'
        )

        self.assertEqual(
            entry_node_body_original.s_expr,
            entry_node_body_copy.s_expr
        )
