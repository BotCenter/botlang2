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


class Val(ASTNode):
    """
    Value expression
    """
    def __init__(self, value):
        super(ASTNode, self).__init__()
        self.value = value

    def accept(self, visitor, env):
        return visitor.visit_val(self, env)


class If(ASTNode):
    """
    'If' construct
    """
    def __init__(self, cond, if_true, if_false):
        super(ASTNode, self).__init__()
        self.cond = cond
        self.if_true = if_true
        self.if_false = if_false

    def accept(self, visitor, env):
        return visitor.visit_if(self, env)


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


class Id(ASTNode):
    """
    Identifier (variable name)
    """
    def __init__(self, identifier):
        super(ASTNode, self).__init__()
        self.identifier = identifier

    def accept(self, visitor, env):
        return visitor.visit_id(self, env)


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


class BodySequence(ASTNode):
    """
    Sequence of expressions
    """
    def __init__(self, expressions):
        super(ASTNode, self).__init__()
        self.expressions = expressions

    def accept(self, visitor, env):
        return visitor.visit_body(self, env)


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
