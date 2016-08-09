from core.botcenter_dsl import BotcenterDSL
from core.parser import Parser


class BotcenterREPL(object):

    def exit_function(self):
        def repl_exit():
            self.active = False

        return repl_exit

    def __init__(self):

        self.active = True
        self.dsl = BotcenterDSL()
        self.dsl.environment.add_primitives(
            {'exit': self.exit_function()}
        )

    @classmethod
    def input(cls, prompt):
        '''
        Disgusting trick, because of python's decision of renaming raw_input
        to input in version 3
        '''
        if hasattr(__builtins__, 'raw_input'):
            return raw_input(prompt)
        else:
            return input(prompt)

    def eval(self, code_string):
        try:
            ast = Parser.parse(code_string)
            return self.dsl.interpret(ast)
        except Exception as e:
            name = e.__class__.__name__
            message = e.args[0]
            return '{0}: {1}'.format(name, message)

    @classmethod
    def run(cls):
        print('Welcome to the BotCenter REPL\n')
        runtime = BotcenterREPL()
        line_breaks = 0
        code_input = ''

        while runtime.active:

            if line_breaks == 0:
                prompt = '>> '
            else:
                prompt = '\t'

            code_input += cls.input(prompt)
            balanced, fail_index = Parser.balanced_parens(code_input)
            if not balanced and fail_index == len(code_input):
                line_breaks += 1
                continue

            value = runtime.eval(code_input)
            if value is not None:
                print(value)
            line_breaks = 0
            code_input = ''


if __name__ == '__main__':
    BotcenterREPL.run()
