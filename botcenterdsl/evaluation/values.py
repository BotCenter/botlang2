class FunVal(object):
    """
    First-order function values
    """
    def __call__(self, *args):
        return self.apply(*args)

    def apply(self, *args):
        raise NotImplementedError('Must implement apply(*args)')

    def is_bot_node(self):
        return False

    def is_primitive(self):
        return False


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
        return '<built-in function {0}>'.format(self.env.get_function_name(self))

    def is_primitive(self):
        return True


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
        new_bindings = {
            self.params[i]: v for i, v in enumerate(values)
        }
        return self.body.accept(
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
        name = self.env.get_function_name(self)

        if name is None:
            return '<anonymous bot-node>'

        return '<bot-node {0} at {1}>'.format(name, hex(id(self)))

    def is_bot_node(self):
        return True


class BotResultValue(object):

    BOT_WAITING_INPUT = 'WAITING_INPUT'

    def __init__(
            self,
            data,
            message,
            next_node,
            evaluation_state
    ):

        self.data = data
        self.message = message
        self.execution_state = evaluation_state

        if next_node.is_bot_node():
            self.next_node = next_node
            self.bot_state = self.BOT_WAITING_INPUT
        else:
            self.next_node = None
            self.bot_state = next_node()
