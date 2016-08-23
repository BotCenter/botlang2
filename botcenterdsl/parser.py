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
        return Fun(
            [identifier.code for identifier in self.children[1].children],
            BodySequence(
                [s_expr.to_ast() for s_expr in self.children[2:]]
            ).add_code_reference(self)
        ).add_code_reference(self)

    def bot_node(self):
        return BotNode(
            [identifier.code for identifier in self.children[1].children],
            BodySequence(
                [s_expr.to_ast() for s_expr in self.children[2:]]
            ).add_code_reference(self)
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


class Parser(object):

    @classmethod
    def parse(cls, code):
        """
        :param code: BotcenterDSL code string to parse
        :rtype: ASTNode
        """
        balanced, failure_index = cls.balanced_parens(code)
        if not balanced:
            raise SyntaxError('unbalanced parentheses')

        s_expressions = Parser(code).s_expressions()
        abstract_syntax_trees = [s_expr.to_ast() for s_expr in s_expressions]
        return BodySequence(abstract_syntax_trees)

    FIND_STRINGS_REGEX = re.compile('"[^"]*"')

    def __init__(self, code):

        self.code = code
        self.strings = {}

        string_index = 0
        for match in self.FIND_STRINGS_REGEX.finditer(code):
            identifier = '__REPLACED_STR__{0}'.format(string_index)
            self.strings[identifier] = match.group(0)
            self.code = self.code.replace(
                match.group(0),
                identifier
            )
            string_index += 1

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
                parens_stack.append((index, current_line))

            if char in SExpression.CLOSING_PARENS:
                start_index, start_line = parens_stack.pop()
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

        return s_expressions

    @classmethod
    def balanced_parens(cls, string):
        """
        Returns a (<balanced>, <index>) tuple in which <balanced> is a
        boolean that represents whether <string> has balanced parentheses.
        If <balanced> is true, <index> is None. If <balanced> is false, <index>
        is an integer value indicating the index in <string> that caused the
        checking to fail.
        """
        stack = []
        i = 0

        for char in string:
            if char in SExpression.OPENING_PARENS:
                stack.append(char)

            if char in SExpression.CLOSING_PARENS:
                if len(stack) == 0:
                    return False, i

                paren_index = SExpression.CLOSING_PARENS.index(char)
                if stack.pop() != SExpression.OPENING_PARENS[paren_index]:
                    return False, i
            i += 1

        if len(stack) > 0:
            return False, i

        return True, None
