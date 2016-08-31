class Visitor(object):
    """
    AST visitor base class
    """

    def visit_val(self, val_node, env):
        """
        Value expression
        """
        raise NotImplementedError

    def visit_if(self, if_node, env):
        """
        'If' construct
        """
        raise NotImplementedError

    def visit_and(self, and_node, env):
        """
        Logical 'and'
        """
        raise NotImplementedError

    def visit_or(self, or_node, env):
        """
        Logical 'or'
        """
        raise NotImplementedError

    def visit_id(self, id_node, env):
        """
        Identifier (variable name)
        """
        raise NotImplementedError

    def visit_fun(self, fun_node, env):
        """
        Function expression
        """
        raise NotImplementedError

    def visit_app(self, app_node, env):
        """
        Function application
        """
        raise NotImplementedError

    def visit_body(self, body_node, env):
        """
        Sequence of expressions
        """
        raise NotImplementedError

    def visit_definition(self, def_node, env):
        """
        Definition
        """
        raise NotImplementedError

    def visit_local(self, local_node, env):
        """
        Local definition
        """
        raise NotImplementedError
