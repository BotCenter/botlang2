from botlang.ast.ast import *


class Visitor(object):
    """
    AST visitor base class
    """

    def visit_val(self, val_node: Val, env):

        return val_node

    def visit_list(self, literal_list: ListVal, env):

        return [
            element.accept(self, env) for element in literal_list.elements
        ]

    def visit_if(self, if_node: If, env):

        if_node.cond.accept(self, env)
        if_node.if_true.accept(self, env)
        if_node.if_false.accept(self, env)
        return if_node

    def visit_cond(self, cond_node: Cond, env):

        for clause in cond_node.cond_clauses:
            clause.accept(self, env)
        return cond_node

    def visit_cond_predicate_clause(
            self,
            predicate_node: CondPredicateClause,
            env
    ):
        predicate_node.predicate.accept(self, env)
        predicate_node.then_body.accept(self, env)
        return predicate_node

    def visit_cond_else_clause(self, else_node: CondElseClause, env):
        return else_node.then_body.accept(self, env)

    def visit_and(self, and_node: And, env):

        and_node.cond1.accept(self, env)
        and_node.cond2.accept(self, env)
        return and_node

    def visit_or(self, or_node: Or, env):

        or_node.cond1.accept(self, env)
        or_node.cond2.accept(self, env)
        return or_node

    def visit_id(self, id_node: Id, env):

        return id_node

    def visit_fun(self, fun_node: Fun, env):

        return fun_node.body.accept(self, env)

    def visit_app(self, app_node: App, env):

        app_node.fun_expr.accept(self, env)
        for argument in app_node.arg_exprs:
            argument.accept(self, env)
        return app_node

    def visit_body(self, body_node: BodySequence, env):

        for expression in body_node.expressions:
            expression.accept(self, env)
        return body_node

    def visit_definition(self, def_node: Definition, env):

        return def_node.expr.accept(self, env)

    def visit_local(self, local_node: Local, env):

        for definition in local_node.definitions:
            definition.accept(self, env)
        local_node.body.accept(self, env)
        return local_node

    def visit_module_definition(self, module_node: ModuleDefinition, env):

        return module_node.body.accept(self, env)

    def visit_module_import(self, require_node: ModuleImport, env):

        return require_node

    def visit_module_function_export(
            self,
            provide_node: ModuleFunctionExport,
            env
    ):
        return provide_node
