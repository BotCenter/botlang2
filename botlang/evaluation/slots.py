from botlang.evaluation.values import ReturnNode


def return_node(environment, inner_node):
    try:
        environment.lookup(Slots.DIGRESSION_RETURN)
    except NameError:
        return inner_node
    else:
        return ReturnNode(inner_node)


class Slots(object):

    CURRENT_SLOTS_NODE = '__CURRENT_SLOTS_NODE__'
    DIGRESSION_RETURN = '__DIGRESSION_RETURN_NODE__'

    SLOTS_FUNCTIONS = {
        'return': return_node
    }

    @classmethod
    def get_base_environment(cls, environment):

        base_env = environment
        while base_env.previous is not None:
            base_env = base_env.previous
        return base_env

    @classmethod
    def digression_started(cls, environment):

        base_env = cls.get_base_environment(environment)
        return base_env.bindings.get(Slots.DIGRESSION_RETURN, False)

    @classmethod
    def start_digression(cls, environment):

        base_env = cls.get_base_environment(environment)
        base_env.bindings[Slots.DIGRESSION_RETURN] = True

    @classmethod
    def end_digression(cls, environment):

        base_env = cls.get_base_environment(environment)
        del base_env.bindings[Slots.DIGRESSION_RETURN]
