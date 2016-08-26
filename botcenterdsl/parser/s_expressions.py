from botcenterdsl.ast.ast import *


class SExpression(object):
    """
    https://en.wikipedia.org/wiki/S-expression
    """
    OPENING_PARENS = ['(', '[', '{']
    CLOSING_PARENS = [')', ']', '}']

    def to_ast(self):
        raise NotImplementedError


class Atom(SExpression):

    def __init__(self, token, line):

        self.code = token
        self.start_line = line
        self.end_line = line

    def to_ast(self):

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
                return self.string_or_symbol(
                    self.code
                ).add_code_reference(self)

    @classmethod
    def string_or_symbol(cls, token):

        if token.startswith('"') and token.endswith('"'):
            return Val(token[1:-1].replace('\\n', '\n'))
        if token.startswith("'"):
            return Val(token[1:])
        return Id(token)


class Tree(SExpression):

    def __init__(self, children, code, start_line, end_line):

        self.children = children
        self.code = code
        self.start_line = start_line
        self.end_line = end_line

    def to_ast(self):

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
