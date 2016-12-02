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
        'If' conditional
        """
        raise NotImplementedError

    def visit_cond(self, cond_node, env):
        """
        'Cond' conditional
        """
        raise NotImplementedError

    def visit_cond_predicate_clause(self, predicate_node, env):
        """
        'Cond' predicate clause node
        """
        raise NotImplementedError

    def visit_cond_else_clause(self, else_node, env):
        """
        'Cond' else clause node
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

    def visit_module_definition(self, module_node, env):
        """
        Module definition
        """
        raise NotImplementedError

    def visit_module_import(self, require_node, env):
        """
        Module import
        """
        raise NotImplementedError

    def visit_module_function_export(self, provide_node, env):
        """
        Module function's export
        """
        raise NotImplementedError
