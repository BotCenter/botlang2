class Nil(object):
    pass


class FunVal(object):
    """
    First-order function values
    """
    def __call__(self, *args):
        return self.apply(*args)

    def apply(self, *args):
        raise NotImplementedError('Must implement apply(*args)')


class Primitive(FunVal):
    """
    Primitive function
    """
    def __init__(self, proc, env):
        self.proc = proc
        self.env = env

    def apply(self, *args):
        return self.proc(*args)

    def __repr__(self):
        return '<built-in function {0}>'.format(
            self.env.get_function_name(self)
        )


class InvalidArgumentsException(Exception):

    def __init__(self, expected, given):
        super(Exception, self).__init__(
            'function expects {0} arguments, {1} given'.format(
                expected,
                given
            )
        )


class Closure(FunVal):
    """
    Lexical closure
    """
    def __init__(self, ast_node, env, evaluator):
        self.params = ast_node.params
        self.body = ast_node.body
        self.env = env
        self.evaluator = evaluator
        self.ast_node = ast_node

    def apply(self, *values):

        if len(self.params) != len(values):
            raise InvalidArgumentsException(len(self.params), len(values))

        from botlang import BotlangSystem
        new_bindings = {
            self.params[i]: v for i, v in enumerate(values)
        }
        return BotlangSystem.interpret(
            [self.body],
            self.evaluator,
            self.env.new_environment(new_bindings)
        )

    def __repr__(self):
        name = self.env.get_function_name(self)

        if name is None:
            return '<anonymous function>'

        return '<function {0} at {1}>'.format(name, hex(id(self)))


class BotNodeValue(Closure):
    """
    Bot node (also a lexical closure)
    """
    def __repr__(self):
        name = self.name()
        if name is None:
            return '<anonymous bot-node>'

        return '<bot-node {0} at {1}>'.format(name, hex(id(self)))

    def name(self):
        return self.env.get_function_name(self)

    def is_terminal(self):
        return False


class TerminalNode(object):

    def __init__(self, state):
        self.state = state

    def is_terminal(self):
        return True


class BotResultValue(object):

    BOT_WAITING_INPUT = 'WAITING_INPUT'

    def __init__(
            self,
            data,
            message,
            next_node
    ):
        self.data = data
        self.message = message

        if next_node.is_terminal():
            self.next_node = None
            self.bot_state = next_node.state
        else:
            self.next_node = next_node.name()
            self.bot_state = self.BOT_WAITING_INPUT
