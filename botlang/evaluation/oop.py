import copy

from botlang.evaluation.values import FunVal, Nil


class AttributeNotFound(Exception):
    pass


class MessageNotUnderstood(Exception):
    pass


class ConstructorArgumentsMismatch(Exception):
    pass


CLASS_NAME_KEY = 'NAME'
SUPERCLASS_KEY = 'SUPERCLASS'
CLASS_ATTRS_KEY = 'CLASS_ATTRS'
CLASS_METHODS_KEY = 'CLASS_METHODS'
INSTANCE_ATTRS_KEY = 'INSTANCE_ATTRS'
METHODS_KEY = 'METHODS'
CLASS_REFERENCE_KEY = '__CLASS__'
SUPER_CONTEXT = '__SUPER_CONTEXT__'


def default_serialize_object(obj):

    serialized = {
        key: value for key, value in obj.items()
        if key != CLASS_REFERENCE_KEY
    }
    serialized[CLASS_REFERENCE_KEY] = obj[CLASS_REFERENCE_KEY][CLASS_NAME_KEY]
    return serialized


class OopHelper(object):

    OBJECT_CLASS_NAME = 'Object'

    OBJECT_METHODS = {
        'init': lambda self: Nil,
        'serialize': default_serialize_object
    }

    OBJECT_CLASS_METHODS = {}

    BASE_CLASS = {
        CLASS_NAME_KEY: OBJECT_CLASS_NAME,
        SUPERCLASS_KEY: None,
        INSTANCE_ATTRS_KEY: {},
        METHODS_KEY: OBJECT_METHODS,
        CLASS_ATTRS_KEY: {},
        CLASS_METHODS_KEY: OBJECT_CLASS_METHODS
    }

    @classmethod
    def build_class(
            cls,
            name,
            superclass,
            instance_attrs,
            methods,
            class_attrs,
            class_methods
    ):
        return {
            CLASS_NAME_KEY: name,
            SUPERCLASS_KEY: superclass,
            INSTANCE_ATTRS_KEY: instance_attrs,
            METHODS_KEY: methods,
            CLASS_ATTRS_KEY: class_attrs,
            CLASS_METHODS_KEY: class_methods
        }

    @classmethod
    def class_lookup(cls, class_name, environment):

        if class_name == cls.OBJECT_CLASS_NAME:
            return cls.BASE_CLASS
        return environment.lookup(class_name)

    @classmethod
    def collect_instance_attributes(cls, class_obj):

        superclass = class_obj[SUPERCLASS_KEY]
        if superclass is not None:
            acc_attrs = cls.collect_instance_attributes(superclass)
            class_attrs = class_obj[INSTANCE_ATTRS_KEY]
            for key, value in class_attrs.items():
                acc_attrs[key] = value
            return acc_attrs
        else:
            return copy.deepcopy(class_obj[INSTANCE_ATTRS_KEY])

    @classmethod
    def create_instance(cls, class_ref, *args):

        instance = {
            CLASS_REFERENCE_KEY: class_ref
        }
        for key, value in cls.collect_instance_attributes(class_ref).items():
            if not isinstance(value, FunVal):
                instance[key] = copy.deepcopy(value)

        cls.call_constructor(instance, *args)
        return instance

    @classmethod
    def call_constructor(cls, obj, *args):

        try:
            cls.call_method(obj, 'init', *args)
        except Exception as e:
            if 'positional argument' in e.args[0]:
                raise ConstructorArgumentsMismatch(
                    "Constructor arguments don't match"
                )
            else:
                raise e

    @classmethod
    def get_attribute(cls, obj, attribute_name):

        if cls.is_instance(obj):
            return obj[attribute_name]
        else:
            return cls.lookup_in_class(obj, attribute_name, CLASS_ATTRS_KEY)

    @classmethod
    def set_attribute(cls, obj, attribute_name, value):

        if cls.is_instance(obj):
            obj[attribute_name] = value
        else:
            obj[CLASS_ATTRS_KEY][attribute_name] = value
        return obj

    @classmethod
    def lookup_in_class(cls, class_obj, attribute_name, attributes_key):

        method = class_obj.get(attributes_key, {}).get(attribute_name)
        if method is None:
            superclass = class_obj.get(SUPERCLASS_KEY)
            if superclass is None:
                raise AttributeNotFound(
                    'Attribute "{}" not found'.format(attribute_name)
                )
            else:
                return cls.method_lookup(superclass, attribute_name)
        else:
            return method

    @classmethod
    def method_lookup(cls, class_obj, method_name, methods_key=METHODS_KEY):
        try:
            return cls.lookup_in_class(class_obj, method_name, methods_key)
        except AttributeNotFound:
            raise MessageNotUnderstood(
                'Message "{}" not understood'.format(method_name)
            )

    @classmethod
    def call_classmethod(cls, class_obj, method_name, *args):

        method = cls.method_lookup(class_obj, method_name, CLASS_METHODS_KEY)
        return method(class_obj, *args)

    @classmethod
    def is_instance(cls, obj):

        return obj.get(CLASS_REFERENCE_KEY) is not None

    @classmethod
    def call_method(cls, obj, method_name, *args):

        if not cls.is_instance(obj):
            return cls.call_classmethod(obj, method_name, *args)

        # Method could have been overridden at instance level
        fun = obj.get(method_name)
        if fun is not None:
            method = fun(obj, *args)
        else:
            class_obj = obj[CLASS_REFERENCE_KEY]
            method = cls.method_lookup(class_obj, method_name)

        return method(obj, *args)

    @classmethod
    def call_parent_method(cls, obj, method_name, *args):

        super_context = obj.get(SUPER_CONTEXT)
        if super_context is None:
            obj[SUPER_CONTEXT] = []
            superclass_obj = obj[CLASS_REFERENCE_KEY][SUPERCLASS_KEY]
        else:
            superclass_obj = super_context[-1][SUPERCLASS_KEY]

        obj[SUPER_CONTEXT].append(superclass_obj)
        method = cls.method_lookup(superclass_obj, method_name)
        result = method(obj, *args)
        obj[SUPER_CONTEXT].pop()

        if len(obj[SUPER_CONTEXT]) == 0:
            del obj[SUPER_CONTEXT]
        return result
