from botlang import Evaluator
from botlang.interpreter import BotlangSystem
from botlang.parser import Parser


class BotlangREPL(object):

    def exit_function(self):
        def repl_exit():
            self.active = False

        return repl_exit

    def __init__(self):

        self.active = True
        self.dsl = BotlangSystem()
        self.dsl.environment.add_primitives(
            {'exit': self.exit_function()}
        )

    @classmethod
    def input(cls, prompt):
        """
        Disgusting trick, because of python's decision of renaming raw_input
        to input in version 3
        """
        if hasattr(__builtins__, 'raw_input'):
            return raw_input(prompt)
        else:
            return input(prompt)

    def eval(self, code_string):
        try:
            ast_seq = Parser.parse(code_string)
            return BotlangSystem.interpret(
                ast_seq,
                Evaluator(),
                self.dsl.environment
            )
        except Exception as e:
            name = e.__class__.__name__
            return '{0}: {1}'.format(name, e.message)

    @classmethod
    def balanced_parens(cls, code):

        opening_parens = ['(', '[']
        closing_parens = [')', ']']
        parens_stack = []

        for char in code:
            try:
                opening_parens.index(char)
                parens_stack.append(char)
            except ValueError:
                pass

            try:
                closing_index = closing_parens.index(char)
                matching = parens_stack.pop()
                opening_index = opening_parens.index(matching)
                if closing_index != opening_index:
                    return False
            except ValueError:
                pass

        if len(parens_stack) > 0:
            return False

        return True

    @classmethod
    def run(cls):
        print('Welcome to the BotCenter REPL\n')
        runtime = BotlangREPL()
        line_breaks = 0
        code_input = ''

        while runtime.active:

            if line_breaks == 0:
                prompt = '>> '
            else:
                prompt = '\t'

            code_input += cls.input(prompt) + ' '
            balanced = cls.balanced_parens(code_input)
            if not balanced:
                line_breaks += 1
                continue

            value = runtime.eval(code_input)
            if value is not None:
                print(value)
            line_breaks = 0
            code_input = ''


if __name__ == '__main__':
    BotlangREPL.run()
