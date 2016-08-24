import base64
import hashlib
import re

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

    def string_or_symbol(self, token):

        if token.startswith('"') and token.endswith('"'):
            return Val(token[1:-1])
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


class BotLangSyntaxError(Exception):

    def __init__(self, message):
        super(Exception, self).__init__(message)


class Parser(object):

    @classmethod
    def parse(cls, code):
        """
        :param code: BotcenterDSL code string to parse
        :rtype: list[ASTNode]
        """
        s_expressions = Parser(code).s_expressions()
        abstract_syntax_trees = [s_expr.to_ast() for s_expr in s_expressions]
        return abstract_syntax_trees

    FIND_STRINGS_REGEX = re.compile('"[^"]*"')

    def __init__(self, code):

        self.code = code
        self.strings = {}

        for match in self.FIND_STRINGS_REGEX.finditer(code):
            string = match.group(0)
            str_hash = self.generate_string_hash(string)
            identifier = '__STR__{0}'.format(str_hash)
            self.strings[identifier] = string
            self.code = self.code.replace(
                string,
                identifier
            )

    @classmethod
    def generate_string_hash(cls, string):

        try:
            encoded_str = string.encode('utf-8')
        except UnicodeDecodeError:
            encoded_str = string
        return base64.b64encode(hashlib.md5(encoded_str).hexdigest())

    def s_expressions(self):

        return self.s_expressions_from_string(self.code)

    def restore_code(self, code):

        restored_code = code
        for key, value in self.strings.items():
            restored_code = restored_code.replace(key, value)
        return restored_code

    def restore_token(self, token):

        restored_token = self.strings.get(token)
        if restored_token is not None:
            return restored_token
        return token

    @classmethod
    def parens_match(cls, open_paren, closed_paren):

        return SExpression.OPENING_PARENS.index(open_paren) ==\
            SExpression.CLOSING_PARENS.index(closed_paren)

    @classmethod
    def raise_unbalanced_parens(cls, line):

        raise BotLangSyntaxError(
            'unbalanced parentheses, line {0}'.format(line)
        )

    def s_expressions_from_string(self, s_expr_string, current_line=1):

        s_expressions = []
        parens_stack = []
        last_index = 0
        current_index = 0

        for index, char in enumerate(s_expr_string):

            if char in [' ', '\t', '\n'] and len(parens_stack) == 0:
                token = s_expr_string[last_index:index].strip()

                if len(token) > 0:
                    s_expressions.append(
                        Atom(self.restore_token(token), current_line)
                    )
                    last_index = index + 1

            if char == '\n':
                current_line += 1

            if char in SExpression.OPENING_PARENS:
                parens_stack.append((index, current_line, char))

            if char in SExpression.CLOSING_PARENS:
                try:
                    start_index, start_line, paren = parens_stack.pop()
                    if not self.parens_match(paren, char):
                        self.raise_unbalanced_parens(current_line)
                except IndexError:
                    self.raise_unbalanced_parens(current_line)

                if len(parens_stack) == 0:
                    code = self.restore_code(
                        s_expr_string[start_index:index+1].strip()
                    )
                    s_expr = Tree(
                        self.s_expressions_from_string(
                            s_expr_string[start_index+1:index],
                            start_line
                        ),
                        code,
                        start_line,
                        current_line
                    )
                    s_expressions.append(s_expr)
                    last_index = index + 1

            current_index = index + 1

        if current_index > last_index:
            token = s_expr_string[last_index:].strip()
            if len(token) > 0:
                s_expressions.append(
                    Atom(self.restore_token(token), current_line)
                )

        if len(parens_stack) > 0:
            self.raise_unbalanced_parens(current_line)

        return s_expressions
