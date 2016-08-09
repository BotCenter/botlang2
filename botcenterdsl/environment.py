from botcenterdsl.evaluation.evaluator import Primitive


class Environment(object):
    """
    Environment (scope)
    """
    def __init__(self, bindings=None, previous=None):
        self.previous = previous
        self.bindings = bindings if bindings is not None else {}
        self.names = {id(obj): name for name, obj in self.bindings.items()}

    def lookup(self, var_name):
        result = self.bindings.get(var_name, None)
        if result is not None:
            return result
        if self.previous:
            return self.previous.lookup(var_name)
        raise NameError("name '{0}' is not defined".format(var_name))

    def get_name(self, obj):
        name = self.names.get(obj)
        if name is not None:
            return name
        if self.previous:
            return self.previous.get_name(obj)

    def update(self, bindings):
        self.bindings.update(bindings)
        self.names.update({obj: name for name, obj in bindings.items()})
        return self

    def add_primitives(self, bindings):
        return self.update(
            {k: Primitive(v, self) for k, v in bindings.items()}
        )

    def new_environment(self, bindings=None):
        return Environment(
            bindings if bindings is not None else {},
            previous=self
        )
