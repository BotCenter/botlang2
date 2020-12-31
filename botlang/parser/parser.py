import base64
import hashlib
import re

from botlang.macros.macro_expander import MacroExpander
from botlang.parser.bot_definition_checker import BotDefinitionChecker
from botlang.parser.s_expressions import *
from botlang.parser.source_reference import SourceReference


class Parser(object):

    @classmethod
    def parse(cls, code, source_id=None, expand_macros=True):
        """
        :param code: Botlang code string to parse
        :param source_id: source code identifier (e.g.: filename)
        :param expand_macros: should expand macros?
        :rtype: list[ASTNode]
        """
        s_expressions = Parser(code, source_id).s_expressions()
        abstract_syntax_trees = [
            cls.s_expr_to_ast(s_expr) for s_expr in s_expressions
        ]

        if expand_macros:
            abstract_syntax_trees = cls.expand_macros(abstract_syntax_trees)

        return abstract_syntax_trees

    @classmethod
    def expand_macros(cls, ast_seq):

        from botlang.macros.default_macros import DefaultMacros
        macro_environment = DefaultMacros.get_environment()
        expanded_asts = [
            ast.accept(MacroExpander(), macro_environment) for ast in ast_seq
        ]
        return expanded_asts

    @classmethod
    def s_expr_to_ast(cls, s_expr):

        ast = s_expr.to_ast()
        ast.accept(BotDefinitionChecker(), None)
        return ast

    FIND_STRINGS_REGEX = re.compile(r'"(?:\\"|[^"])*?"')

    def __init__(self, code, source_id=None):

        if source_id is None:
            source_id = '<unknown>'

        self.code = code
        self.source_id = source_id
        self.strings = {}
        self.hash_strings()
        self.code = self.remove_comments(self.code)

    REMOVE_COMMENTS_REGEX = re.compile(r"(;+.*)")

    def remove_comments(self, code):

        for match in self.REMOVE_COMMENTS_REGEX.finditer(code):
            comment = match.group(1)
            code = code.replace(comment, ' ' * len(comment))
        return code

    def hash_strings(self):

        for match in self.FIND_STRINGS_REGEX.finditer(self.code):
            string = match.group(0)
            str_hash = self.generate_string_hash(string)
            identifier = '__STR__{0}'.format(str_hash)
            self.strings[identifier] = string
            pattern = r'(^|\s|\(|\[)({})(\s|$|\)|\])'.format(re.escape(string))
            self.code = re.sub(
                pattern,
                lambda m: '{}{}{}'.format(m.group(1), identifier, m.group(3)),
                self.code
            )

    @classmethod
    def generate_string_hash(cls, string):

        try:
            encoded_str = string.encode('utf-8')
        except UnicodeDecodeError:
            encoded_str = string

        md5_hash = hashlib.md5(encoded_str).hexdigest()
        return base64.b64encode(md5_hash.encode('utf-8')).decode('utf-8')

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
    def raise_unbalanced_parens(cls, reason, line):

        raise BotLangSyntaxError(
            'Unbalanced parentheses: {}, line {}'.format(reason, line)
        )

    @classmethod
    def is_quoted(cls, string, opening_paren_index):

        try:
            char = string[opening_paren_index-1]
        except IndexError:
            return False

        return char == '\''

    def add_atom(self, state, token):
        state.s_expressions.append(
            Atom(
                self.restore_token(token),
                SourceReference(
                    self.source_id,
                    state.current_line,
                    state.current_line
                )
            )
        )
        return state

    def parse_next_char(self, state, index, char):

        if char in [' ', '\t', '\n'] and len(state.parens_stack) == 0:
            token = state.s_expr_string[state.last_index:index].strip()
            if len(token) > 0:
                self.add_atom(state, token)
                state.last_index = index + 1

        if char == '\n':
            state.current_line += 1

        if char in SExpression.OPENING_PARENS:
            state.parens_stack.append((index, state.current_line, char))

        if char in SExpression.CLOSING_PARENS:
            try:
                start_index, start_line, paren = state.parens_stack.pop()
                if not self.parens_match(paren, char):
                    self.raise_unbalanced_parens(
                        "opening and closing symbols don't match",
                        state.current_line
                    )
            except IndexError:
                self.raise_unbalanced_parens(
                    'excess closing symbol',
                    state.current_line
                )
            else:
                if len(state.parens_stack) == 0:
                    code = self.restore_code(
                        state.s_expr_string[start_index:index + 1].strip()
                    )
                    s_expr = Tree(
                        self.s_expressions_from_string(
                            state.s_expr_string[start_index + 1:index],
                            start_line
                        ),
                        code,
                        SourceReference(
                            self.source_id,
                            start_line,
                            state.current_line
                        ),
                        quoted=self.is_quoted(state.s_expr_string, start_index)
                    )
                    state.s_expressions.append(s_expr)
                    state.last_index = index + 1

        state.current_index = index + 1

    def s_expressions_from_string(self, s_expr_string, current_line=1):

        state = ParsingState(s_expr_string, current_line)

        for current_index, current_char in enumerate(s_expr_string):
            self.parse_next_char(state, current_index, current_char)

        if state.current_index > state.last_index:
            token = s_expr_string[state.last_index:].strip()
            if len(token) > 0:
                self.add_atom(state, token)

        if len(state.parens_stack) > 0:
            self.raise_unbalanced_parens('not closed', state.current_line)

        return state.s_expressions


class ParsingState(object):

    def __init__(self, s_expr_string, current_line):
        self.s_expr_string = s_expr_string
        self.current_line = current_line
        self.s_expressions = []
        self.parens_stack = []
        self.last_index = 0
        self.current_index = 0
