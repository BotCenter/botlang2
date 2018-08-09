from botlang.evaluation.oop import OopHelper


def new_instance(cls, *args):
    return OopHelper.create_instance(cls, *args)


def get_attribute(obj, attribute_name):
    return obj[attribute_name]


def set_attribute(obj, attribute_name, value):
    obj[attribute_name] = value
    return obj


def call_method(obj, method_name, *args):
    return OopHelper.call_method(obj, method_name, *args)


OOP_PRIMITIVES = {
    'new': new_instance,
    '@!': set_attribute,
    '@': get_attribute,
    '@@': call_method,
    'send': call_method
}
