from botlang.parser.s_expressions import Tree


class SExprVisitor(object):

    def visit_atom(self, atom_node):

        return atom_node

    def visit_tree(self, tree_node):

        return Tree(
            [child.accept(self) for child in tree_node.children],
            tree_node.code,
            tree_node.source_reference,
            tree_node.quoted
        )
