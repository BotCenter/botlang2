class ASTNode(object):
    """
    Language expression
    """
    def accept(self, visitor, environment):
        raise NotImplementedError(
            'Must implement accept(visitor, environment)'
        )

    def __init__(self):
        self.s_expr = None

    def add_code_reference(self, code_reference):
        self.s_expr = code_reference
        return self

    def print_node_type(self):
        raise NotImplementedError


class Val(ASTNode):
    """
    Value expression
    """
    def __init__(self, value):
        super(ASTNode, self).__init__()
        self.value = value

    def accept(self, visitor, env):
        return visitor.visit_val(self, env)

    def print_node_type(self):
        return 'value'


class ListVal(ASTNode):
    """
    Literal list expression
    """
    def __init__(self, elements):
        super(ASTNode, self).__init__()
        self.elements = elements

    def accept(self, visitor, env):
        return visitor.visit_list(self, env)

    def print_node_type(self):
        return 'list'


class If(ASTNode):
    """
    'If' conditional
    """
    def __init__(self, cond, if_true, if_false):
        super(ASTNode, self).__init__()
        self.cond = cond
        self.if_true = if_true
        self.if_false = if_false

    def accept(self, visitor, env):
        return visitor.visit_if(self, env)

    def print_node_type(self):
        return 'if node'


class Cond(ASTNode):
    """
    'Cond' conditional
    """
    def __init__(self, cond_clauses):
        super(ASTNode, self).__init__()
        self.cond_clauses = cond_clauses

    def accept(self, visitor, environment):
        return visitor.visit_cond(self, environment)

    def print_node_type(self):
        return 'cond node'


class CondPredicateClause(ASTNode):
    """
    'Cond' predicate clause
    """
    def __init__(self, predicate, then_body):
        super(ASTNode, self).__init__()
        self.predicate = predicate
        self.then_body = then_body

    def accept(self, visitor, environment):
        return visitor.visit_cond_predicate_clause(self, environment)

    def print_node_type(self):
        return 'cond clause'


class CondElseClause(ASTNode):
    """
    'Cond' else clause
    """
    def __init__(self, then_body):
        super(ASTNode, self).__init__()
        self.then_body = then_body

    def accept(self, visitor, environment):
        return visitor.visit_cond_else_clause(self, environment)

    def print_node_type(self):
        return 'else clause'


class And(ASTNode):
    """
    Logical 'and'
    """
    def __init__(self, cond1, cond2):
        super(ASTNode, self).__init__()
        self.cond1 = cond1
        self.cond2 = cond2

    def accept(self, visitor, env):
        return visitor.visit_and(self, env)

    def print_node_type(self):
        return 'and node'


class Or(ASTNode):
    """
    Logical 'or'
    """
    def __init__(self, cond1, cond2):
        super(ASTNode, self).__init__()
        self.cond1 = cond1
        self.cond2 = cond2

    def accept(self, visitor, env):
        return visitor.visit_or(self, env)

    def print_node_type(self):
        return 'or node'


class Id(ASTNode):
    """
    Identifier (variable name)
    """
    def __init__(self, identifier):
        super(ASTNode, self).__init__()
        self.identifier = identifier

    def accept(self, visitor, env):
        return visitor.visit_id(self, env)

    def print_node_type(self):
        return 'identifier lookup'


class Fun(ASTNode):
    """
    Function expression
    """
    def __init__(self, params, body):
        super(ASTNode, self).__init__()
        self.params = params
        self.body = body

    def accept(self, visitor, env):
        return visitor.visit_fun(self, env)

    def print_node_type(self):
        return 'function definition'


class App(ASTNode):
    """
    Function application
    """
    def __init__(self, fun_expr, arg_exprs):
        super(ASTNode, self).__init__()
        self.fun_expr = fun_expr
        self.arg_exprs = arg_exprs

    def accept(self, visitor, env):
        return visitor.visit_app(self, env)

    def print_node_type(self):
        return 'function application'


class BodySequence(ASTNode):
    """
    Sequence of expressions
    """
    def __init__(self, expressions):
        super(ASTNode, self).__init__()
        self.expressions = expressions

    def accept(self, visitor, env):
        return visitor.visit_body(self, env)

    def print_node_type(self):
        return 'expressions body'


class ModuleDefinition(ASTNode):
    """
    Module definition
    """
    def __init__(self, name, body):
        super(ASTNode, self).__init__()
        self.name = name
        self.body = body

    def accept(self, visitor, environment):
        return visitor.visit_module_definition(self, environment)

    def print_node_type(self):
        return 'module definition'


class ModuleFunctionExport(ASTNode):
    """
    Module function's export
    """
    def __init__(self, identifiers_to_export):
        super(ASTNode, self).__init__()
        self.identifiers_to_export = identifiers_to_export

    def accept(self, visitor, environment):
        return visitor.visit_module_function_export(self, environment)

    def print_node_type(self):
        return 'module function export'


class ModuleImport(ASTNode):
    """
    Module import
    """
    def __init__(self, module_name):
        super(ASTNode, self).__init__()
        self.module_name = module_name

    def accept(self, visitor, environment):
        return visitor.visit_module_import(self, environment)

    def print_node_type(self):
        return 'module import'


class Definition(ASTNode):
    """
    Definition
    """
    def __init__(self, name, expr):
        super(ASTNode, self).__init__()
        self.name = name
        self.expr = expr

    def accept(self, visitor, env):
        return visitor.visit_definition(self, env)

    def print_node_type(self):
        return 'definition'


class Local(ASTNode):
    """
    Local definition
    """
    def __init__(self, definitions, body):
        super(ASTNode, self).__init__()
        self.definitions = definitions
        self.body = body

    def accept(self, visitor, env):
        return visitor.visit_local(self, env)

    def print_node_type(self):
        return 'local definition'


class BotNode(ASTNode):
    """
    Bot node expression
    """
    def __init__(self, data, body):
        super(ASTNode, self).__init__()
        self.params = data
        self.body = body

    def accept(self, visitor, env):
        return visitor.visit_bot_node(self, env)

    def print_node_type(self):
        return 'bot node expression'


class BotResult(ASTNode):
    """
    Bot node computation result.
    """
    def __init__(self, data, message, next_node):
        super(ASTNode, self).__init__()
        self.data = data
        self.message = message
        self.next_node = next_node

    def accept(self, visitor, env):
        return visitor.visit_bot_result(self, env)

    def print_node_type(self):
        return 'bot result'
