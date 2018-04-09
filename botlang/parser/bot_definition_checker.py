from botlang.ast.ast_visitor import ASTVisitor


class BotDefinitionChecker(ASTVisitor):

    def __init__(self):

        self.depth = 0

    def visit_bot_node(self, bot_node, env):

        if self.depth > 0:
            raise InvalidBotDefinitionException(
                'Bots can only be defined at module level'
            )
        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_bot_node(bot_node, env)
        self.depth -= 1
        return r

    def visit_list(self, literal_list, env):

        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_list(literal_list, env)
        self.depth -= 1
        return r

    def visit_if(self, if_node, env):

        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_if(if_node, env)
        self.depth -= 1
        return r

    def visit_cond(self, visit_cond, env):

        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_cond(visit_cond, env)
        self.depth -= 1
        return r

    def visit_cond_predicate_clause(self, predicate_node, env):

        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_cond_predicate_clause(
            predicate_node,
            env
        )
        self.depth -= 1
        return r

    def visit_cond_else_clause(self, else_node, env):

        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_cond_else_clause(
            else_node,
            env
        )
        self.depth -= 1
        return r

    def visit_and(self, and_node, env):

        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_and(and_node, env)
        self.depth -= 1
        return r

    def visit_or(self, or_node, env):

        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_or(or_node, env)
        self.depth -= 1
        return r

    def visit_fun(self, fun_node, env):

        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_fun(fun_node, env)
        self.depth -= 1
        return r

    def visit_bot_result(self, bot_result, env):

        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_bot_result(bot_result, env)
        self.depth -= 1
        return r

    def visit_app(self, app_node, env):

        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_app(app_node, env)
        self.depth -= 1
        return r

    def visit_local(self, local_node, env):

        self.depth += 1
        r = super(BotDefinitionChecker, self).visit_local(local_node, env)
        self.depth -= 1
        return r


class InvalidBotDefinitionException(Exception):
    pass
