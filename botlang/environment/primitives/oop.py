import copy

from botlang.evaluation.values import FunVal

CLASS_REFERENCE_KEY = '__CLASS__'


def new_instance(cls, *args):

    instance = {
        CLASS_REFERENCE_KEY: cls
    }
    for key, value in cls['members'].items():
        if not isinstance(value, FunVal):
            instance[key] = copy.deepcopy(value)

    # call_method(instance, 'init', *args)    # Constructor call
    return instance


def get_attribute(obj, attribute_name):
    return obj[attribute_name]


def set_attribute(obj, attribute_name, value):
    obj[attribute_name] = value
    return obj


def call_method(obj, method_name, *args):

    method = obj[CLASS_REFERENCE_KEY].get('members', {}).get(method_name)
    return method(obj, *args)


OOP_PRIMITIVES = {
    'new': new_instance,
    '@!': set_attribute,
    '@': get_attribute,
    '@@': call_method
}
