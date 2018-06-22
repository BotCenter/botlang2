from botlang.evaluation.values import FunVal


class BotlangReflectionException(Exception):
    pass


def reflect_get(environment, identifier):
    return environment.lookup(identifier)


def reflect_get_node(environment, node_id):
    node = reflect_get(environment, node_id)
    from botlang import BotNodeValue
    if not isinstance(node, BotNodeValue):
        raise BotlangReflectionException(
            "'{}' is not a bot node".format(node_id)
        )
    return node


def reflect_get_fun(environment, node_id):
    fun = reflect_get(environment, node_id)
    if not isinstance(fun, FunVal):
        raise BotlangReflectionException(
            "'{}' is not a function".format(node_id)
        )
    return fun


REFLECTIVE_PRIMITIVES = {
    'get-node': reflect_get_node,
    'reflect-get': reflect_get,
    'reflect-get-fun': reflect_get_fun,
    'reflect-get-node': reflect_get_node
}
