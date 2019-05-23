import ast as python_ast
from botlang.ast.ast import *
from botlang.evaluation.oop import OopHelper
from botlang.evaluation.values import Nil


class SExpression(object):
    """
    https://en.wikipedia.org/wiki/S-expression
    """
    OPENING_PARENS = ['(', '[', '{']
    CLOSING_PARENS = [')', ']', '}']

    def to_ast(self):
        raise NotImplementedError

    def accept(self, visitor):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    @classmethod
    def is_tree(cls):
        return False

    @classmethod
    def is_atom(cls):
        return False


class Atom(SExpression):

    @classmethod
    def is_atom(cls):
        return True

    def __init__(self, token, source_reference):

        self.code = token
        self.source_reference = source_reference

    def __repr__(self):

        return 'Atom({})'.format(self.code)

    def accept(self, visitor):
        return visitor.visit_atom(self)

    def copy(self):
        return Atom(self.code, self.source_reference)

    @property
    def token(self):
        return self.code

    def to_ast(self, quoted_parent=False):

        try:
            return self.as_boolean_value()
        except ValueError:
            pass

        try:
            return self.as_integer_value()
        except ValueError:
            pass

        try:
            return self.as_float_value()
        except ValueError:
            pass

        if self.is_string():
            return self.as_string_value()

        if self.is_symbol() or quoted_parent:
            return self.as_symbol_value(quoted_parent)

        return self.as_identifier()

    def is_boolean(self):

        return self.code == '#t' or self.code == '#f'

    def is_integer(self):

        try:
            self.as_integer_value()
        except ValueError:
            return False
        else:
            return True

    def is_float(self):

        try:
            self.as_float_value()
        except ValueError:
            return False
        else:
            return True

    def is_number(self):

        return self.is_integer() or self.is_float()

    def is_identifier(self):

        return \
            not self.is_boolean() \
            and not self.is_number() \
            and not self.is_string() \
            and not self.is_symbol()

    def as_boolean_value(self):

        if self.code == '#t':
            return Val(True).add_code_reference(self)

        if self.code == '#f':
            return Val(False).add_code_reference(self)

        raise ValueError

    def as_integer_value(self):

        return Val(int(self.code)).add_code_reference(self)

    def as_float_value(self):

        return Val(float(self.code)).add_code_reference(self)

    def as_quoted(self):

        return self.to_ast(quoted_parent=True)

    def as_string_value(self):

        return Val(
            python_ast.literal_eval(self.code.replace('\n', '\\n'))
        ).add_code_reference(self)

    def as_symbol_value(self, quoted_parent):

        symbol = self.token if quoted_parent else self.token[1:]
        return Val(symbol).add_code_reference(self)

    def as_identifier(self):

        return Id(self.token).add_code_reference(self)

    def is_string(self):

        return self.code.startswith('"') and self.code.endswith('"')

    def is_symbol(self):

        return self.code.startswith("'")


class Tree(SExpression):

    @classmethod
    def is_tree(cls):
        return True

    def __init__(self, children, code, source_reference, quoted=False):

        self.children = children
        self.code = code
        self.source_reference = source_reference
        self.quoted = quoted

    def __repr__(self):

        return 'Tree({})'.format(self.children)

    def accept(self, visitor):
        return visitor.visit_tree(self)

    def copy(self):

        return Tree(
            [child.copy() for child in self.children],
            self.code,
            self.source_reference,
            self.quoted
        )

    def as_quoted(self):

        return ListVal([
            child.as_quoted() for child in self.children
        ]).add_code_reference(self)

    def to_ast(self):

        if self.quoted or len(self.children) == 0:
            return self.as_quoted()

        first = self.children[0].code

        if first == 'if':
            return self.if_node()

        if first == 'cond':
            return self.cond_node()

        if first == 'defclass':
            return self.class_definition_node()

        if first == 'and':
            return self.and_node()

        if first == 'or':
            return self.or_node()

        if first == 'define':
            return self.define_node()

        if first == 'local':
            return self.local_node()

        if first == 'begin':
            return self.begin_node()

        if first == 'fun' or first == 'function':
            return self.function_node(self.children)

        if first == 'bot-node':
            return self.bot_node()

        if first == 'slots-node':
            return self.slots_node()

        if first == 'node-result':
            return self.bot_result_node()

        if first == 'module':
            return self.module_definition_node()

        if first == 'provide':
            return self.module_export_node()

        if first == 'require':
            return self.module_import_node()

        if first == 'define-syntax-rule':
            return self.define_syntax_rule_node()

        return self.application_node()

    def module_definition_node(self):

        module_body = BodySequence(
            [s_expr.to_ast() for s_expr in self.children[2:]]
        ).add_code_reference(self)

        return ModuleDefinition(
            self.children[1].to_ast(),
            module_body
        ).add_code_reference(self)

    def module_export_node(self):

        return ModuleFunctionExport(
            [identifier.to_ast() for identifier in self.children[1:]]
        ).add_code_reference(self)

    def module_import_node(self):

        return ModuleImport(
            self.children[1].to_ast()
        ).add_code_reference(self)

    def if_node(self):

        return If(
            self.children[1].to_ast(),
            self.children[2].to_ast(),
            self.children[3].to_ast() if len(self.children) > 3 else Val(Nil)
        ).add_code_reference(self)

    def cond_node(self):

        return Cond(
            [child.to_cond_clause_ast_node() for child in self.children[1:]]
        ).add_code_reference(self)

    def to_cond_clause_ast_node(self):

        first = self.children[0].code

        if first == 'else':
            return CondElseClause(
                self.children[1].to_ast()
            ).add_code_reference(self)

        return CondPredicateClause(
            self.children[0].to_ast(),
            self.children[1].to_ast()
        ).add_code_reference(self)

    def class_definition_node(self):

        properties = self.children[2:]
        superclass = self.get_superclass(properties)

        attributes = self.get_instance_attributes(properties)
        class_attributes = self.get_class_attributes(properties)

        methods = self.get_instance_methods(properties)
        class_methods = self.get_class_methods(properties)

        return ClassDefinition(
            self.children[1].code,
            superclass,
            attributes,
            methods,
            class_attributes,
            class_methods
        ).add_code_reference(self)

    @classmethod
    def get_superclass(cls, properties):
        try:
            extends = [
                expr.children[1].code
                for expr in properties if expr.children[0].code == 'extends'
            ]
            return extends[0]
        except IndexError:
            return OopHelper.OBJECT_CLASS_NAME

    @classmethod
    def get_attributes(cls, class_properties, attributes_key):
        try:
            attributes_def = [
                expr.children[1:] for expr in class_properties
                if expr.children[0].code == attributes_key
            ][0]
            return [
                AttributeDefinition(
                    child.children[0].code,
                    child.children[1].to_ast()
                ) if child.is_tree()
                else AttributeDefinition(child.code, None)
                for child in attributes_def
            ]
        except IndexError:
            return []

    @classmethod
    def get_instance_attributes(cls, class_properties):
        return cls.get_attributes(class_properties, 'attributes')

    @classmethod
    def get_class_attributes(cls, class_properties):
        return cls.get_attributes(class_properties, 'class-attributes')

    @classmethod
    def get_methods(cls, class_properties, methods_key):
        try:
            return [
                [
                    MethodDefinition(
                        child.children[0].code,
                        child.children[1].to_ast()
                    )
                    for child in expr.children[1:]
                ]
                for expr in class_properties
                if expr.children[0].code == methods_key
            ][0]
        except IndexError:
            return []

    @classmethod
    def get_instance_methods(cls, class_properties):
        return cls.get_methods(class_properties, 'methods')

    @classmethod
    def get_class_methods(cls, class_properties):
        return cls.get_methods(class_properties, 'class-methods')

    def and_node(self):

        return And(
            [child.to_ast() for child in self.children[1:]]
        ).add_code_reference(self)

    def or_node(self):

        return Or(
            [child.to_ast() for child in self.children[1:]]
        ).add_code_reference(self)

    def define_node(self):

        return Definition(
            self.children[1].code,
            self.children[2].to_ast()
        ).add_code_reference(self)

    def local_node(self):

        return Local(
            [
                Definition(
                    d.children[0].code,
                    d.children[1].to_ast()
                ).add_code_reference(d)

                for d in self.children[1].children
            ],
            self.children[2].to_ast()
        ).add_code_reference(self)

    def begin_node(self):

        return BodySequence(
            [s_expr.to_ast() for s_expr in self.children[1:]]
        ).add_code_reference(self)

    def function_node(self, children):

        function_body = BodySequence(
            [s_expr.to_ast() for s_expr in children[2:]]
        ).add_code_reference(self)

        return Fun(
            [identifier.code for identifier in children[1].children],
            function_body
        ).add_code_reference(self)

    def bot_node(self):

        bot_node_body = BodySequence(
            [s_expr.to_ast() for s_expr in self.children[2:]]
        ).add_code_reference(self)

        return BotNode(
            [identifier.code for identifier in self.children[1].children],
            bot_node_body
        ).add_code_reference(self)

    def slots_node(self):

        node_name = self.children[1].token
        args = [identifier.token for identifier in self.children[2].children]

        blocks = self.children[3:]
        self.check_slots_node_blocks(blocks)

        before = self.get_slots_before(blocks)
        digress = self.get_slots_digress(blocks)
        slots = self.get_slots(blocks)
        then = self.get_slots_then(blocks)

        slots_node_body = SlotsNodeBody(
            args, before, digress, slots, then
        ).add_code_reference(self)

        return BotSlotsNode(node_name, args, slots_node_body)\
            .add_code_reference(self)

    @classmethod
    def get_slots_before(cls, blocks):

        for block in blocks:
            if block.children[0].token == 'before':
                return block.children[1].to_ast()
        return None

    @classmethod
    def get_slots_digress(cls, blocks):

        for block in blocks:
            if block.children[0].token == 'digress':
                return block.children[1].to_ast()
        return None

    @classmethod
    def get_slots(cls, blocks):

        return [
            block.to_slot_ast_node() for block in blocks
            if block.children[0].token == 'slot'
        ]

    @classmethod
    def get_slots_then(cls, blocks):

        for block in blocks:
            if block.children[0].token == 'then':
                return block.children[1].to_ast()
        raise SyntaxError("The 'then' block is required for slot nodes")

    @classmethod
    def check_slots_node_blocks(cls, blocks):

        for block in blocks:
            token = block.children[0].token
            if token not in ['before', 'digress', 'slot', 'then']:
                raise SyntaxError('Unknown slots node block: %s' % token)

    def to_slot_ast_node(self):

        return SlotDefinition(
            self.children[1].token,
            self.children[2].token,
            self.children[3].to_ast(),
            self.children[4].to_ast() if len(self.children) > 4 else None
        ).add_code_reference(self)

    def bot_result_node(self):

        return BotResult(
            self.children[1].to_ast(),
            self.children[2].to_ast(),
            self.children[3].to_ast()
        ).add_code_reference(self)

    def application_node(self):

        return App(
            self.children[0].to_ast(),
            [s_expr.to_ast() for s_expr in self.children[1:]]
        ).add_code_reference(self)

    def define_syntax_rule_node(self):

        pattern = self.children[1].children
        pattern_node = SyntaxPattern(pattern[0], pattern[1:])
        return DefineSyntax(
            pattern_node.add_code_reference(pattern_node),
            self.children[2]
        ).add_code_reference(self)
