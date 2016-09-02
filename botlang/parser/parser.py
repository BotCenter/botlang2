import base64
import hashlib
import re

from botlang.parser.s_expressions import *


class BotLangSyntaxError(Exception):

    def __init__(self, message):
        super(Exception, self).__init__(message)


class Parser(object):

    asts_cache = {}

    @classmethod
    def parse(cls, code):
        """
        :param code: Botlang code string to parse
        :rtype: list[ASTNode]
        """
        code_id = cls.generate_string_hash(code)
        cached_asts = cls.asts_cache.get(code_id)

        if cached_asts is not None:
            return cached_asts

        s_expressions = Parser(code).s_expressions()
        abstract_syntax_trees = [s_expr.to_ast() for s_expr in s_expressions]
        cls.asts_cache[code_id] = abstract_syntax_trees

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

        md5_hash = hashlib.md5(encoded_str).hexdigest()
        return base64.b64encode(md5_hash.encode('utf-8'))

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

    @classmethod
    def is_quoted(cls, string, opening_paren_index):

        try:
            char = string[opening_paren_index-1]
        except IndexError:
            return False

        return char == '\''

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
                        current_line,
                        quoted=self.is_quoted(s_expr_string, start_index)
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
