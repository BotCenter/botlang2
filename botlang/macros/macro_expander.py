from botlang.ast.ast import Id
from botlang.ast.ast_visitor import ASTVisitor
from botlang.parser.s_expressions_visitor import SExprVisitor


class MacroArgumentsDontMatchException(Exception):

    def __init__(self, args_expected, args_received):
        super(MacroArgumentsDontMatchException, self).__init__()
        self.args_expected = args_expected
        self.args_received = args_received


class MacroExpander(ASTVisitor):

    def visit_app(self, app_node, env):

        if isinstance(app_node.fun_expr, Id):
            macro_def = self.get_macro_definition(app_node.fun_expr, env)
            if macro_def is not None:
                try:
                    return self.expand_macro(macro_def, app_node.arg_exprs)
                except MacroArgumentsDontMatchException as e:
                    from botlang.parser import BotLangSyntaxError
                    raise BotLangSyntaxError(
                        'Line {}. Expansion of macro {} failed: expected {} '
                        'arguments, got {}'.format(
                            app_node.s_expr.source_reference.start_line,
                            app_node.fun_expr.identifier,
                            e.args_expected,
                            e.args_received
                        )
                    )
        return app_node

    def visit_define_syntax(self, define_syntax_node, env):

        env.update({
            define_syntax_node.pattern.identifier.token: define_syntax_node
        })
        return define_syntax_node

    @classmethod
    def get_macro_definition(cls, id_node, env):
        try:
            return env.lookup(id_node.identifier)
        except NameError:
            return None

    @classmethod
    def expand_macro(cls, macro_definition, arguments):
        """
        1) Get identifiers used in arguments ASTs
        2) Hygienize macro template S-Expr given the arguments' identifiers
        3) Copy arguments S-Expr into hygienized template S-Expr (expansion)
        4) Return expanded macro
        
        :param macro_definition: DefineSyntax
        :param arguments: List[ASTNode]
        :return: 
        """
        if not len(macro_definition.pattern.arguments) == len(arguments):
            raise MacroArgumentsDontMatchException(
                len(macro_definition.pattern.arguments),
                len(arguments)
            )

        identifier_finder = IdentifierFinder()
        for argument in arguments:
            argument.accept(identifier_finder, None)
        identifiers = identifier_finder.identifiers

        pattern = macro_definition.pattern.copy()
        template = macro_definition.template.copy()
        hygienizer = MacroHygienizer(identifiers, pattern)
        hygienic_template = template.accept(hygienizer)

        sexpr_mappings = {}
        for i, arg in enumerate(arguments):
            sexpr_mappings[pattern.arguments[i].token] = arg.s_expr

        expanded = hygienic_template.accept(SExprExpander(sexpr_mappings))
        return expanded.to_ast()


class SExprExpander(SExprVisitor):

    def __init__(self, mappings):

        self.mappings = mappings

    def visit_atom(self, atom_node):

        sexpr_to_paste = self.mappings.get(atom_node.token)
        if sexpr_to_paste is not None:
            return sexpr_to_paste.copy()
        return atom_node


class MacroHygienizer(SExprVisitor):
    """
    https://en.wikipedia.org/wiki/Hygienic_macro
    """
    def __init__(self, existing_identifiers, macro_pattern):

        pattern_arguments = [arg.token for arg in macro_pattern.arguments]
        ids = existing_identifiers.difference(set(pattern_arguments))
        self.existing_identifiers = ids
        self.hygienic_mapping = {}

    def visit_atom(self, atom_node):

        if atom_node.token in self.existing_identifiers:
            replacement = self.hygienic_mapping.get(atom_node.token)
            if replacement is not None:
                atom_node.token = replacement
            else:
                replacement = self.get_replacement_for(atom_node.token)
                self.hygienic_mapping[atom_node.token] = replacement
                atom_node.token = replacement
        return atom_node

    def get_replacement_for(self, identifier):

        counter = 1
        while '{}_{}'.format(identifier, counter) in self.existing_identifiers:
            counter += 1
        return '{}_{}'.format(identifier, counter)


class IdentifierFinder(ASTVisitor):

    def __init__(self):
        self.identifiers = set()

    def visit_id(self, id_node, env):
        self.identifiers.add(id_node.identifier)
