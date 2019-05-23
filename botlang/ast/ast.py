import copy


class ASTNode(object):
    """
    Language expression
    """
    def accept(self, visitor, env):
        """
        :param visitor: an ASTVisitor
        :param env: an Environment
        :return:
        """
        raise NotImplementedError(
            'Must implement accept(visitor, env)'
        )

    def __init__(self):
        self.s_expr = None

    def add_code_reference(self, code_reference):
        self.s_expr = code_reference
        return self

    def print_node_type(self):
        raise NotImplementedError

    def copy(self):
        """
        Deep-copies this AST
        :return: an ASTNode
        """
        raise NotImplementedError


class Val(ASTNode):
    """
    Value expression
    """
    def __init__(self, value):
        """
        :param value: any 
        """
        super(Val, self).__init__()
        self.value = value

    def accept(self, visitor, env):
        return visitor.visit_val(self, env)

    def print_node_type(self):
        return 'value'

    def copy(self):
        return Val(self.value).add_code_reference(self.s_expr)


class ListVal(ASTNode):
    """
    Literal list expression
    """
    def __init__(self, elements):
        """
        :param elements: List[Val]
        """
        super(ListVal, self).__init__()
        self.elements = elements

    def accept(self, visitor, env):
        return visitor.visit_list(self, env)

    def print_node_type(self):
        return 'list'

    def copy(self):
        return ListVal([e.copy() for e in self.elements])\
            .add_code_reference(self.s_expr)


class If(ASTNode):
    """
    'If' conditional
    """
    def __init__(self, cond, if_true, if_false):
        """
        :param cond: ASTNode
        :param if_true: ASTNode
        :param if_false: ASTNode
        """
        super(If, self).__init__()
        self.cond = cond
        self.if_true = if_true
        self.if_false = if_false

    def accept(self, visitor, env):
        return visitor.visit_if(self, env)

    def print_node_type(self):
        return 'if node'

    def copy(self):
        return If(self.cond.copy(), self.if_true.copy(), self.if_false.copy())\
            .add_code_reference(self.s_expr)


class Cond(ASTNode):
    """
    'Cond' conditional
    """
    def __init__(self, cond_clauses):
        """
        :param cond_clauses: List[CondPredicateClause*, CondElseClause]
        """
        super(Cond, self).__init__()
        self.cond_clauses = cond_clauses

    def accept(self, visitor, env):
        return visitor.visit_cond(self, env)

    def print_node_type(self):
        return 'cond node'

    def copy(self):
        return Cond([clause.copy() for clause in self.cond_clauses])\
            .add_code_reference(self.s_expr)


class CondPredicateClause(ASTNode):
    """
    'Cond' predicate clause
    """
    def __init__(self, predicate, then_body):
        """
        :param predicate: ASTNode
        :param then_body: ASTNode
        """
        super(CondPredicateClause, self).__init__()
        self.predicate = predicate
        self.then_body = then_body

    def accept(self, visitor, env):
        return visitor.visit_cond_predicate_clause(self, env)

    def print_node_type(self):
        return 'cond clause'

    def copy(self):
        return CondPredicateClause(
            self.predicate.copy(),
            self.then_body.copy()
        ).add_code_reference(self.s_expr)


class CondElseClause(ASTNode):
    """
    'Cond' else clause
    """
    def __init__(self, then_body):
        """
        :param then_body: ASTNode 
        """
        super(CondElseClause, self).__init__()
        self.then_body = then_body

    def accept(self, visitor, env):
        return visitor.visit_cond_else_clause(self, env)

    def print_node_type(self):
        return 'else clause'

    def copy(self):
        return CondElseClause(self.then_body.copy())\
            .add_code_reference(self.s_expr)


class And(ASTNode):
    """
    Logical 'and'
    """
    def __init__(self, conditions):
        """
        :param conditions: List[ASTNode]
        """
        super(And, self).__init__()
        self.conditions = conditions

    def accept(self, visitor, env):
        return visitor.visit_and(self, env)

    def print_node_type(self):
        return 'and node'

    def copy(self):
        return And([cond.copy() for cond in self.conditions])\
            .add_code_reference(self.s_expr)


class Or(ASTNode):
    """
    Logical 'or'
    """

    def __init__(self, conditions):
        """
        :param conditions: List[ASTNode]
        """
        super(Or, self).__init__()
        self.conditions = conditions

    def accept(self, visitor, env):
        return visitor.visit_or(self, env)

    def print_node_type(self):
        return 'or node'

    def copy(self):
        return Or([cond.copy() for cond in self.conditions])\
            .add_code_reference(self.s_expr)


class Id(ASTNode):
    """
    Identifier (variable name)
    """
    def __init__(self, identifier):
        """
        :param identifier: string 
        """
        super(Id, self).__init__()
        self.identifier = identifier

    def accept(self, visitor, env):
        return visitor.visit_id(self, env)

    def print_node_type(self):
        return 'identifier lookup'

    def copy(self):
        return Id(self.identifier).add_code_reference(self.s_expr)


class Fun(ASTNode):
    """
    Function expression
    """
    def __init__(self, params, body):
        """
        :param params: List[string]
        :param body: BodySequence
        """
        super(Fun, self).__init__()
        self.params = params
        self.body = body

    def accept(self, visitor, env):
        return visitor.visit_fun(self, env)

    def print_node_type(self):
        return 'function definition'

    def copy(self):
        return Fun(
            copy.copy(self.params),
            self.body.copy()
        ).add_code_reference(self.s_expr)


class App(ASTNode):
    """
    Function application
    """
    def __init__(self, fun_expr, arg_exprs):
        """
        :param fun_expr: ASTNode 
        :param arg_exprs: List[ASTNode]
        """
        super(App, self).__init__()
        self.fun_expr = fun_expr
        self.arg_exprs = arg_exprs

    def accept(self, visitor, env):
        return visitor.visit_app(self, env)

    def print_node_type(self):
        return 'function application'

    def copy(self):
        return App(
            self.fun_expr.copy(),
            [arg.copy() for arg in self.arg_exprs]
        ).add_code_reference(self.s_expr)


class BodySequence(ASTNode):
    """
    Sequence of expressions
    """
    def __init__(self, expressions):
        """
        :param expressions: List[ASTNode] 
        """
        super(BodySequence, self).__init__()
        self.expressions = expressions

    def accept(self, visitor, env):
        return visitor.visit_body(self, env)

    def print_node_type(self):
        return 'expressions body'

    def copy(self):
        return BodySequence(
            [expression.copy() for expression in self.expressions]
        ).add_code_reference(self.s_expr)


class ClassDefinition(ASTNode):

    def __init__(
            self,
            class_name,
            superclass_name,
            attributes,
            methods,
            class_attributes,
            class_methods
    ):
        """
        :param class_name: string
        :param superclass_name: string
        :param attributes: List[InstanceAttributeDefinition]
        :param methods: List[MethodDefinition]
        :param class_attributes: List[InstanceAttributeDefinition]
        :param class_methods: List[MethodDefinition]
        """
        super(ClassDefinition, self).__init__()
        self.name = class_name
        self.superclass = superclass_name
        self.attributes = attributes
        self.methods = methods
        self.class_attributes = class_attributes
        self.class_methods = class_methods

    def accept(self, visitor, env):
        return visitor.visit_class_definition(self, env)

    def print_node_type(self):
        return 'class definition'

    def copy(self):
        return ClassDefinition(
            self.name,
            self.superclass,
            self.attributes,
            self.methods,
            self.class_attributes,
            self.class_methods
        ).add_code_reference(self.s_expr)


class AttributeDefinition(ASTNode):

    def __init__(self, identifier, attribute_definition):
        """
        :param identifier: string
        :param attribute_definition: ASTNode
        """
        super(AttributeDefinition, self).__init__()
        self.identifier = identifier
        self.definition = attribute_definition

    def accept(self, visitor, env):
        return visitor.visit_instance_attribute(self, env)

    def print_node_type(self):
        return 'attribute definition'

    def copy(self):
        return AttributeDefinition(
            self.identifier,
            self.definition
        ).add_code_reference(self.s_expr)


class MethodDefinition(ASTNode):

    def __init__(self, identifier, function_definition):
        """
        :param identifier: string
        :param function_definition: Fun
        """
        super(MethodDefinition, self).__init__()
        self.identifier = identifier
        self.definition = function_definition

    def accept(self, visitor, env):
        return visitor.visit_method_definition(self, env)

    def print_node_type(self):
        return 'method definition'

    def copy(self):
        return MethodDefinition(
            self.identifier,
            self.definition
        ).add_code_reference(self.s_expr)


class ModuleDefinition(ASTNode):
    """
    Module definition
    """
    def __init__(self, name, body):
        super(ModuleDefinition, self).__init__()
        self.name = name
        self.body = body

    def accept(self, visitor, env):
        return visitor.visit_module_definition(self, env)

    def print_node_type(self):
        return 'module definition'

    def copy(self):
        return ModuleDefinition(self.name.copy(), self.body.copy())\
            .add_code_reference(self.s_expr)


class ModuleFunctionExport(ASTNode):
    """
    Module function's export
    """
    def __init__(self, identifiers_to_export):
        super(ModuleFunctionExport, self).__init__()
        self.identifiers_to_export = identifiers_to_export

    def accept(self, visitor, env):
        return visitor.visit_module_function_export(self, env)

    def print_node_type(self):
        return 'module function export'

    def copy(self):
        return ModuleFunctionExport(
            [identifier.copy() for identifier in self.identifiers_to_export]
        ).add_code_reference(self.s_expr)


class ModuleImport(ASTNode):
    """
    Module import
    """
    def __init__(self, module_name):
        super(ModuleImport, self).__init__()
        self.module_name = module_name

    def accept(self, visitor, env):
        return visitor.visit_module_import(self, env)

    def print_node_type(self):
        return 'module import'

    def copy(self):
        return ModuleImport(self.module_name).add_code_reference(self.s_expr)


class Definition(ASTNode):
    """
    Definition
    """
    def __init__(self, name, expr):
        """
        :param name: string 
        :param expr: ASTNode
        """
        super(Definition, self).__init__()
        self.name = name
        self.expr = expr

    def accept(self, visitor, env):
        return visitor.visit_definition(self, env)

    def print_node_type(self):
        return 'definition'

    def copy(self):
        return Definition(self.name, self.expr.copy())\
            .add_code_reference(self.s_expr)


class Local(ASTNode):
    """
    Local definition
    """
    def __init__(self, definitions, body):
        """
        :param definitions: List[Definition]
        :param body: BodySequence
        """
        super(Local, self).__init__()
        self.definitions = definitions
        self.body = body

    def accept(self, visitor, env):
        return visitor.visit_local(self, env)

    def print_node_type(self):
        return 'local definition'

    def copy(self):
        return Local(
            [definition.copy() for definition in self.definitions],
            self.body.copy()
        ).add_code_reference(self.s_expr)


class BotNode(ASTNode):
    """
    Bot node expression
    """
    def __init__(self, params, body):
        """
        :param params: List[string] 
        :param body: BodySequence
        """
        super(BotNode, self).__init__()
        self.params = params
        self.body = body

    def accept(self, visitor, env):
        return visitor.visit_bot_node(self, env)

    def print_node_type(self):
        return 'bot node expression'

    def copy(self):
        return BotNode(
            copy.copy(self.params),
            self.body.copy()
        ).add_code_reference(self.s_expr)


class BotResult(ASTNode):
    """
    Bot node computation result.
    """
    def __init__(self, data, message, next_node):
        super(BotResult, self).__init__()
        self.data = data
        self.message = message
        self.next_node = next_node

    def accept(self, visitor, env):
        return visitor.visit_bot_result(self, env)

    def print_node_type(self):
        return 'bot result'

    def copy(self):
        return BotResult(
            self.data.copy(),
            self.message.copy(),
            self.next_node.copy()
        ).add_code_reference(self.s_expr)


class BotSlotsNode(ASTNode):
    """
    BotNode with slots
    """
    def __init__(self, node_name, params, body):
        super(BotSlotsNode, self).__init__()
        self.node_name = node_name
        self.params = params
        self.body = body

    def accept(self, visitor, env):
        return visitor.visit_slots_node(self, env)

    def print_node_type(self):
        return 'bot slots node'

    def copy(self):
        return BotSlotsNode(
            self.node_name, copy.copy(self.params), self.body.copy()
        ).add_code_reference(self.s_expr)


class SlotsNodeBody(ASTNode):

    def __init__(self, params, before, digress, slots, then):
        super(SlotsNodeBody, self).__init__()
        self.params = params
        self.before = before
        self.digress = digress
        self.slots = slots
        self.then = then

    def accept(self, visitor, env):
        return visitor.visit_slots_node_body(self, env)

    def print_node_type(self):
        return 'bot slots node body'

    def copy(self):
        return SlotsNodeBody(
            copy.copy(self.params),
            self.before.copy() if self.before is not None else None,
            self.digress.copy() if self.digress is not None else None,
            [slot.copy for slot in self.slots],
            self.then.copy()
        ).add_code_reference(self.s_expr)


class SlotDefinition(ASTNode):

    def __init__(self, slot_name, context, match_body, ask_body):
        super(SlotDefinition, self).__init__()
        self.slot_name = slot_name
        self.context = context
        self.match_body = match_body
        self.ask_body = ask_body

    def accept(self, visitor, env):
        return visitor.visit_slot_definition(self, env)

    def print_node_type(self):
        return 'slot definition'

    def copy(self):
        return SlotDefinition(
            copy.copy(self.slot_name),
            self.context.copy(),
            self.match_body.copy(),
            self.ask_body.copy() if self.ask_body is not None else None
        ).add_code_reference(self.s_expr)


class SyntaxPattern(ASTNode):
    """
    A pattern in pattern-based macros
    """
    def __init__(self, identifier, arguments):
        """
        :param identifier: string 
        :param arguments: List[string]
        """
        super(SyntaxPattern, self).__init__()
        self.identifier = identifier
        self.arguments = arguments

    def accept(self, visitor, env):
        return visitor.visit_syntax_pattern(self, env)

    def print_node_type(self):
        return 'syntax pattern'

    def copy(self):
        return SyntaxPattern(
            self.identifier,
            copy.copy(self.arguments)
        ).add_code_reference(self.s_expr)


class DefineSyntax(ASTNode):
    """
    Inspired by Racket's define-syntax-rule:
    https://docs.racket-lang.org/guide/pattern-macros.html
    """
    def __init__(self, pattern, template):
        """
        :param pattern: SyntaxPattern
        :param template: SExpr
        """
        super(DefineSyntax, self).__init__()
        self.pattern = pattern
        self.template = template

    def accept(self, visitor, env):
        return visitor.visit_define_syntax(self, env)

    def print_node_type(self):
        return 'syntax definition'

    def copy(self):
        raise NotImplementedError
