import ast as python_ast
from botlang.ast.ast import *


class SExpression(object):
    """
    https://en.wikipedia.org/wiki/S-expression
    """
    OPENING_PARENS = ['(', '[', '{']
    CLOSING_PARENS = [')', ']', '}']

    def to_ast(self):
        raise NotImplementedError

    def accept(self, visitor):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    def is_tree(self):
        return False

    def is_atom(self):
        return False


class Atom(SExpression):

    def __init__(self, token, source_reference):

        self.code = token
        self.source_reference = source_reference

    def accept(self, visitor):
        return visitor.visit_atom(self)

    def copy(self):
        return Atom(self.code, self.source_reference)

    @property
    def token(self):
        return self.code

    def is_atom(self):
        return True

    def to_ast(self, quoted_parent=False):

        try:
            return self.as_boolean_value()
        except ValueError:
            pass

        try:
            return self.as_integer_value()
        except ValueError:
            pass

        try:
            return self.as_float_value()
        except ValueError:
            pass

        if self.is_string():
            return self.as_string_value()

        if self.is_symbol() or quoted_parent:
            return self.as_symbol_value(quoted_parent)

        return self.as_identifier()

    def is_boolean(self):

        return self.code == '#t' or self.code == '#f'

    def is_integer(self):

        try:
            self.as_integer_value()
        except ValueError:
            return False
        else:
            return True

    def is_float(self):

        try:
            self.as_float_value()
        except ValueError:
            return False
        else:
            return True

    def is_number(self):

        return self.is_integer() or self.is_float()

    def is_identifier(self):

        return \
            not self.is_boolean() \
            and not self.is_number() \
            and not self.is_string() \
            and not self.is_symbol()

    def as_boolean_value(self):

        if self.code == '#t':
            return Val(True).add_code_reference(self)

        if self.code == '#f':
            return Val(False).add_code_reference(self)

        raise ValueError

    def as_integer_value(self):

        return Val(int(self.code)).add_code_reference(self)

    def as_float_value(self):

        return Val(float(self.code)).add_code_reference(self)

    def as_quoted(self):

        return self.to_ast(quoted_parent=True)

    def as_string_value(self):

        return Val(
            python_ast.literal_eval(self.code.replace('\n', '\\n'))
        ).add_code_reference(self)

    def as_symbol_value(self, quoted_parent):

        symbol = self.token if quoted_parent else self.token[1:]
        return Val(symbol).add_code_reference(self)

    def as_identifier(self):

        return Id(self.token).add_code_reference(self)

    def is_string(self):

        return self.code.startswith('"') and self.code.endswith('"')

    def is_symbol(self):

        return self.code.startswith("'")


class Tree(SExpression):

    def __init__(self, children, code, source_reference, quoted=False):

        self.children = children
        self.code = code
        self.source_reference = source_reference
        self.quoted = quoted

    def accept(self, visitor):
        return visitor.visit_tree(self)

    def copy(self):

        return Tree(
            [child.copy() for child in self.children],
            self.code,
            self.source_reference,
            self.quoted
        )

    def is_tree(self):
        return True

    def as_quoted(self):

        return ListVal([
            child.as_quoted() for child in self.children
        ]).add_code_reference(self)

    def to_ast(self):

        if self.quoted:
            return self.as_quoted()

        first = self.children[0].code

        if first == 'if':
            return self.if_node()

        if first == 'cond':
            return self.cond_node()

        if first == 'and':
            return self.and_node()

        if first == 'or':
            return self.or_node()

        if first == 'define':
            return self.define_node()

        if first == 'local':
            return self.local_node()

        if first == 'begin':
            return self.begin_node()

        if first == 'fun' or first == 'function':
            return self.function_node(self.children)

        if first == 'bot-node':
            return self.bot_node()

        if first == 'node-result':
            return self.bot_result_node()

        if first == 'module':
            return self.module_definition_node()

        if first == 'provide':
            return self.module_export_node()

        if first == 'require':
            return self.module_import_node()

        if first == 'define-syntax-rule':
            return self.define_syntax_rule_node()

        return self.application_node()

    def module_definition_node(self):

        module_body = BodySequence(
            [s_expr.to_ast() for s_expr in self.children[2:]]
        ).add_code_reference(self)

        return ModuleDefinition(
            self.children[1].to_ast(),
            module_body
        ).add_code_reference(self)

    def module_export_node(self):

        return ModuleFunctionExport(
            [identifier.to_ast() for identifier in self.children[1:]]
        ).add_code_reference(self)

    def module_import_node(self):

        return ModuleImport(
            self.children[1].to_ast()
        ).add_code_reference(self)

    def if_node(self):

        return If(
            self.children[1].to_ast(),
            self.children[2].to_ast(),
            self.children[3].to_ast()
        ).add_code_reference(self)

    def cond_node(self):

        return Cond(
            [child.to_cond_clause_ast_node() for child in self.children[1:]]
        ).add_code_reference(self)

    def to_cond_clause_ast_node(self):

        first = self.children[0].code

        if first == 'else':
            return CondElseClause(
                self.children[1].to_ast()
            ).add_code_reference(self)

        return CondPredicateClause(
            self.children[0].to_ast(),
            self.children[1].to_ast()
        ).add_code_reference(self)

    def and_node(self):

        return And(
            self.children[1].to_ast(),
            self.children[2].to_ast()
        ).add_code_reference(self)

    def or_node(self):

        return Or(
            self.children[1].to_ast(),
            self.children[2].to_ast()
        ).add_code_reference(self)

    def define_node(self):

        return Definition(
            self.children[1].code,
            self.children[2].to_ast()
        ).add_code_reference(self)

    def local_node(self):

        return Local(
            [
                Definition(
                    d.children[0].code,
                    d.children[1].to_ast()
                ).add_code_reference(d)

                for d in self.children[1].children
            ],
            self.children[2].to_ast()
        ).add_code_reference(self)

    def begin_node(self):

        return BodySequence(
            [s_expr.to_ast() for s_expr in self.children[1:]]
        ).add_code_reference(self)

    def function_node(self, children):

        function_body = BodySequence(
            [s_expr.to_ast() for s_expr in children[2:]]
        ).add_code_reference(self)

        return Fun(
            [identifier.code for identifier in children[1].children],
            function_body
        ).add_code_reference(self)

    def bot_node(self):

        bot_node_body = BodySequence(
            [s_expr.to_ast() for s_expr in self.children[2:]]
        ).add_code_reference(self)

        return BotNode(
            [identifier.code for identifier in self.children[1].children],
            bot_node_body
        ).add_code_reference(self)

    def bot_result_node(self):

        return BotResult(
            self.children[1].to_ast(),
            self.children[2].to_ast(),
            self.children[3].to_ast()
        ).add_code_reference(self)

    def application_node(self):

        return App(
            self.children[0].to_ast(),
            [s_expr.to_ast() for s_expr in self.children[1:]]
        ).add_code_reference(self)

    def define_syntax_rule_node(self):

        pattern = self.children[1].children
        pattern_node = SyntaxPattern(pattern[0], pattern[1:])
        return DefineSyntax(
            pattern_node.add_code_reference(pattern_node),
            self.children[2]
        ).add_code_reference(self)
