import copy

from botlang.evaluation.values import FunVal, Nil


class MessageNotUnderstood(Exception):
    pass


CLASS_NAME_KEY = 'NAME'
SUPERCLASS_KEY = 'SUPERCLASS'
INSTANCE_ATTRS_KEY = 'INSTANCE_ATTRS'
METHODS_KEY = 'METHODS'
CLASS_REFERENCE_KEY = '__CLASS__'


def default_serialize_object(obj):

    serialized = {
        key: value for key, value in obj.items()
        if key != CLASS_REFERENCE_KEY
    }
    serialized[CLASS_REFERENCE_KEY] = obj[CLASS_REFERENCE_KEY][CLASS_NAME_KEY]
    return serialized


class OopHelper(object):

    BASE_CLASS_NAME = 'Object'

    BASE_CLASS_METHODS = {
        'init': lambda self: Nil,
        'serialize': default_serialize_object
    }

    BASE_CLASS = {
        CLASS_NAME_KEY: BASE_CLASS_NAME,
        SUPERCLASS_KEY: None,
        INSTANCE_ATTRS_KEY: {},
        METHODS_KEY: BASE_CLASS_METHODS
    }

    @classmethod
    def build_class(cls, name, superclass, instance_attrs, methods):

        return {
            CLASS_NAME_KEY: name,
            SUPERCLASS_KEY: superclass,
            INSTANCE_ATTRS_KEY: instance_attrs,
            METHODS_KEY: methods
        }

    @classmethod
    def class_lookup(cls, class_name, environment):

        if class_name == cls.BASE_CLASS_NAME:
            return cls.BASE_CLASS
        return environment.lookup(class_name)

    @classmethod
    def collect_class_attributes(cls, class_obj):

        superclass = class_obj[SUPERCLASS_KEY]
        if superclass is not None:
            acc_attrs = cls.collect_class_attributes(superclass)
            class_attrs = class_obj[INSTANCE_ATTRS_KEY]
            for key, value in class_attrs.items():
                acc_attrs[key] = value
            return acc_attrs
        else:
            return class_obj[INSTANCE_ATTRS_KEY]

    @classmethod
    def create_instance(cls, class_ref, *args):

        instance = {
            CLASS_REFERENCE_KEY: class_ref
        }
        for key, value in cls.collect_class_attributes(class_ref).items():
            if not isinstance(value, FunVal):
                instance[key] = copy.deepcopy(value)

        cls.call_method(instance, 'init', *args)    # Constructor call
        return instance

    @classmethod
    def method_lookup(cls, class_obj, method_name):

        method = class_obj.get(METHODS_KEY, {}).get(method_name)
        if method is None:
            superclass = class_obj.get(SUPERCLASS_KEY)
            if superclass is None:
                raise MessageNotUnderstood(
                    'Message "{}" not understood'.format(method_name)
                )
            else:
                return cls.method_lookup(superclass, method_name)
        else:
            return method

    @classmethod
    def call_method(cls, obj, method_name, *args):

        # Method could have been overridden at instance level
        fun = obj.get(method_name)
        if fun is not None:
            method = fun(obj, *args)
        else:
            class_obj = obj[CLASS_REFERENCE_KEY]
            method = cls.method_lookup(class_obj, method_name)

        return method(obj, *args)
