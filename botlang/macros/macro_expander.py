from botlang.ast.ast import Id
from botlang.ast.ast_visitor import ASTVisitor


class MacroExpander(ASTVisitor):

    def visit_app(self, app_node, env):

        if isinstance(app_node.fun_expr, Id):
            macro_def = self.get_macro_definition(app_node.fun_expr, env)
            if macro_def is not None:
                return self.expand_macro(macro_def, app_node.arg_exprs)
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
        2) Hygienize macro template AST given the arguments' identifiers
        3) Copy arguments ASTs into hygienized template AST (macro expansion)
        4) Return expanded macro
        
        :param macro_definition: DefineSyntax
        :param arguments: List[ASTNode]
        :return: 
        """
        assert len(macro_definition.pattern.arguments) == len(arguments)

        identifier_finder = IdentifierFinder()
        for argument in arguments:
            argument.accept(identifier_finder, None)
        identifiers = identifier_finder.identifiers

        pattern = macro_definition.pattern.copy()
        template = macro_definition.template.copy()
        hygienizer = MacroHygienizer(identifiers, pattern)
        hygienic_template = template.accept(hygienizer, None)

        ast_mappings = {}
        for i in range(0, len(arguments)):
            ast_mappings[pattern.arguments[i].token] = arguments[i]
        return hygienic_template.accept(ASTExpander(ast_mappings), None)


class ASTExpander(ASTVisitor):

    def __init__(self, mappings):

        self.mappings = mappings

    def visit_id(self, id_node, env):

        ast_to_paste = self.mappings.get(id_node.identifier)
        if ast_to_paste is not None:
            return ast_to_paste.copy()
        else:
            return id_node


class MacroHygienizer(ASTVisitor):

    def __init__(self, existing_identifiers, macro_pattern):

        pattern_arguments = [arg.token for arg in macro_pattern.arguments]
        ids = existing_identifiers.difference(set(pattern_arguments))
        self.existing_identifiers = ids
        self.hygienic_mapping = {}

    def visit_id(self, id_node, env):

        if id_node.identifier in self.existing_identifiers:
            replacement = self.hygienic_mapping.get(id_node.identifier)
            if replacement is not None:
                id_node.identifier = replacement
            else:
                replacement = self.get_replacement_for(id_node.identifier)
                self.hygienic_mapping[id_node.identifier] = replacement
                id_node.identifier = replacement
        return id_node

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
