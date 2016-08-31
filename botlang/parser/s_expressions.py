from botlang.ast.ast import *


class SExpression(object):
    """
    https://en.wikipedia.org/wiki/S-expression
    """
    OPENING_PARENS = ['(', '[', '{']
    CLOSING_PARENS = [')', ']', '}']

    def to_ast(self):
        raise NotImplementedError

    def is_tree(self):
        return False

    def is_atom(self):
        return False


class Atom(SExpression):

    def __init__(self, token, line):

        self.code = token
        self.start_line = line
        self.end_line = line

    def is_atom(self):

        return True

    def to_ast(self, quoted_parent=False):

        if self.code in ['true', '#t']:
            return Val(True).add_code_reference(self)

        if self.code in ['false', '#f']:
            return Val(False).add_code_reference(self)

        try:
            return Val(int(self.code)).add_code_reference(self)

        except ValueError:
            try:
                return Val(float(self.code)).add_code_reference(self)

            except ValueError:
                if self.is_string(self.code):
                    return self.as_string_value(self.code)
                if self.is_symbol(self.code) or quoted_parent:
                    return self.as_symbol_value(self.code, quoted_parent)
                return self.as_identifier(self.code)

    def as_quoted(self):

        return self.to_ast(quoted_parent=True)

    def as_string_value(self, token):

        return Val(token[1:-1].replace('\\n', '\n')).add_code_reference(self)

    def as_symbol_value(self, token, quoted_parent):

        symbol = token if quoted_parent else token[1:]
        return Val(symbol).add_code_reference(self)

    def as_identifier(self, token):

        return Id(token).add_code_reference(self)

    @classmethod
    def is_string(cls, token):

        return token.startswith('"') and token.endswith('"')

    @classmethod
    def is_symbol(cls, token):

        return token.startswith("'")


class Tree(SExpression):

    def __init__(self, children, code, start_line, end_line, quoted=False):

        self.children = children
        self.code = code
        self.start_line = start_line
        self.end_line = end_line
        self.quoted = quoted

    def is_tree(self):

        return True

    def as_quoted(self):

        return ListVal([
            child.as_quoted() for child in self.children
        ])

    def to_ast(self):

        if self.quoted:
            return self.as_quoted()

        first = self.children[0].code

        if first == 'if':
            return self.if_node()

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
            return self.function_node()

        if first == 'bot-node':
            return self.bot_node()

        if first == 'node-result':
            return self.bot_result_node()

        return self.application_node()

    def if_node(self):

        return If(
            self.children[1].to_ast(),
            self.children[2].to_ast(),
            self.children[3].to_ast()
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

    def function_node(self):

        function_body = BodySequence(
            [s_expr.to_ast() for s_expr in self.children[2:]]
        ).add_code_reference(self)

        return Fun(
            [identifier.code for identifier in self.children[1].children],
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
