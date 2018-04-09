from botlang.evaluation.values import *


class Environment(object):
    """
    Environment (scope)
    """
    def __init__(self, bindings=None, previous=None):
        self.previous = previous
        self.bindings = bindings if bindings is not None else {}
        self.function_names = {
            id(obj): name for name, obj in self.bindings.items()
        }
        self.last_input_message = None

    def get_last_input_message(self):

        msg = self.last_input_message
        if msg is not None:
            return msg
        if self.previous:
            return self.previous.get_last_input_message()

    def lookup(self, var_name):
        result = self.bindings.get(var_name, None)
        if result is not None:
            return result
        if self.previous:
            return self.previous.lookup(var_name)
        raise NameError("name '{0}' is not defined".format(var_name))

    def get_function_name(self, obj):
        name = self.function_names.get(obj)
        if name is not None:
            return name
        if self.previous:
            return self.previous.get_function_name(obj)

    def update(self, bindings):
        self.bindings.update(bindings)
        self.function_names.update({
            obj: name for name, obj in bindings.items()
            if isinstance(obj, FunVal)
        })
        return self

    def add_primitives(self, bindings):
        return self.update(
            {k: Primitive(v, self) for k, v in bindings.items()}
        )

    def add_terminal_nodes(self, node_states):

        return self.add_primitives(
            {key: lambda: value for key, value in node_states.items()}
        )

    def new_environment(self, bindings=None):
        return Environment(
            bindings if bindings is not None else {},
            previous=self
        )
