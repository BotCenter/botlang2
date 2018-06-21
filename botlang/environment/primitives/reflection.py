class BotlangReflectionException(Exception):
    pass


def get_node(environment, node_id):
    node = environment.lookup(node_id)

    from botlang import BotNodeValue
    if not isinstance(node, BotNodeValue):
        raise BotlangReflectionException(
            "'{}' is not a bot node".format(node_id)
        )

    return node


REFLECTIVE_PRIMITIVES = {
    'get-node': get_node
}
