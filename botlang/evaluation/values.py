class Nil(object):
    pass


class NativeException(object):
    """
    Object representation of a botlang exception.
    """
    def __init__(self, name='Exception', description='exception'):
        self.name = name
        self.description = description

    def get_type(self):
        return self.name

    def description(self):
        return self.description


class FunVal(object):
    """
    First-order function values
    """
    def __call__(self, *args):
        return self.apply(*args)

    def apply(self, *args):
        raise NotImplementedError('Must implement apply(*args)')

    def is_reflective(self):
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
        return '<built-in function {0}>'.format(
            self.env.get_function_name(self)
        )


class ReflectivePrimitive(Primitive):
    """
    Function that has direct access to the current environment
    """
    def apply(self, evaluation_env, *args):
        return self.proc(evaluation_env, *args)

    def is_reflective(self):
        return True


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


class DialogNode(object):

    def is_terminal(self):
        raise NotImplementedError

    def is_digression_return(self):
        return False


class BotNodeValue(Closure, DialogNode):
    """
    Bot node (also a lexical closure)
    """
    def apply(self, context, message=None):
        if message is not None and len(self.params) == 2:
            return super(BotNodeValue, self).apply(context, message)
        else:
            return super(BotNodeValue, self).apply(context)

    def __repr__(self):
        name = self.name()
        if name is None:
            return '<anonymous bot-node>'

        return '<bot-node {0} at {1}>'.format(name, hex(id(self)))

    def name(self):
        return self.env.get_function_name(self)

    def is_terminal(self):
        return False


class SlotsNodeValue(BotNodeValue):
    """
    Slots node
    """
    def __init__(self, slots_node, env, evaluator):
        from botlang.evaluation.slots import Slots
        env = env.new_environment({Slots.CURRENT_SLOTS_NODE: self})
        super(SlotsNodeValue, self).__init__(slots_node, env, evaluator)

    def __repr__(self):
        name = self.name()
        if name is None:
            return '<anonymous slots-node>'

        return '<slots-node {0} at {1}>'.format(name, hex(id(self)))


class TerminalNode(DialogNode):

    def __init__(self, state):
        self.state = state

    def is_terminal(self):
        return True

    def name(self):
        return None


class ReturnNode(DialogNode):
    """
    Node used for returning to a slot node after a digression.
    """
    def __init__(self, inner_node):
        self.inner_node = inner_node

    def is_terminal(self):
        return False

    def is_digression_return(self):
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
        elif next_node.is_digression_return():
            from botlang.evaluation.slots import Slots
            self.next_node = Slots.DIGRESSION_RETURN
        else:
            self.next_node = next_node.name()
            self.bot_state = self.BOT_WAITING_INPUT

    def __repr__(self):
        return 'BotResult({}, {}, {})'.format(
            self.data, self.message, self.next_node
        )
