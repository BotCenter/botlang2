from botcenterdsl.ast.visitor import Visitor
from botcenterdsl.evaluation.values import *


class ExecutionState(object):

    def __init__(self, primitives_values, bot_node_steps):

        self.primitives_values = primitives_values
        self.bot_node_steps = bot_node_steps


class Evaluator(Visitor):
    """
    AST visitor for evaluation
    """
    def __init__(self, evaluation_state=None):

        if evaluation_state is not None:
            self.primitives_evaluations = evaluation_state.primitives_values[:]
            self.bot_result_skips = evaluation_state.bot_node_steps
        else:
            self.primitives_evaluations = []
            self.bot_result_skips = 0

        self.primitive_step = 0
        self.bot_node_step = 0

    def visit_val(self, val_node, env):
        """
        Value expression evaluation
        """
        return val_node.value

    def visit_if(self, if_node, env):
        """
        'If' construct evaluation
        """
        if if_node.cond.accept(self, env):
            return if_node.if_true.accept(self, env)
        else:
            return if_node.if_false.accept(self, env)

    def visit_and(self, and_node, env):
        """
        Logical 'and' evaluation
        """
        return and_node.cond1.accept(self, env)\
               and and_node.cond2.accept(self, env)

    def visit_or(self, or_node, env):
        """
        Logical 'or' evaluation
        """
        return or_node.cond1.accept(self, env)\
               or or_node.cond2.accept(self, env)

    def visit_id(self, id_node, env):
        """
        Identifier (variable name) resolution
        """
        return env.lookup(id_node.identifier)

    def visit_fun(self, fun_node, env):
        """
        Function expression evaluation.
        Returns closure
        """
        return Closure(fun_node, env, self)

    def visit_bot_node(self, bot_node, env):
        """
        Bot node expression evaluation.
        Returns bot-node closure
        """
        return BotNodeValue(bot_node, env, self)

    def visit_bot_result(self, bot_result, env):
        """
        Bot result evaluation. Returns a BotResultValue which can be used
        to resume execution in the future.

        If the bot_result_skips number configured for this evaluator is
        greater or equal than the current bot_node_step, instead of returning
        a BotResultValue the next node is evaluated immediately.
        """
        data = bot_result.data.accept(self, env)
        message = bot_result.message.accept(self, env)
        next_node = bot_result.next_node.accept(self, env)
        self.bot_node_step += 1

        if self.bot_node_step <= self.bot_result_skips:
            return next_node.apply(data)
        else:
            evaluation_state = ExecutionState(
                self.primitives_evaluations,
                self.bot_node_step
            )
            return BotResultValue(
                data,
                message,
                next_node,
                evaluation_state
            )

    def visit_app(self, app_node, env):
        """
        Function application evaluation. If the function being applied is a
        primitive we check if its value is already stored in this evaluator.
        If it's not, then the value is computed and stored in the
        primitives_evaluation list.
        """
        fun_val = app_node.fun_expr.accept(self, env)
        arg_vals = [arg.accept(self, env) for arg in app_node.arg_exprs]
        if fun_val.is_primitive():
            if self.primitive_step == len(self.primitives_evaluations):
                return_value = fun_val.apply(*arg_vals)
                self.primitives_evaluations.append(return_value)
                self.primitive_step += 1
                return return_value
            else:
                return_value = self.primitives_evaluations[self.primitive_step]
                self.primitive_step += 1
                return return_value

        return fun_val.apply(*arg_vals)

    def visit_body(self, body_node, env):
        """
        Evaluation of a sequence of expressions
        """
        for expr in body_node.expressions[0:-1]:
            expr.accept(self, env)
        return body_node.expressions[-1].accept(self, env)

    def visit_definition(self, def_node, env):
        """
        Definition evaluation.

        Mutates the environment with this definition.
        Evaluates the definition body with the same environment
        that is mutated, which allows recursion.
        Doesn't return a value.
        """
        env.update({def_node.name: def_node.expr.accept(self, env)})

    def visit_local(self, local_node, env):
        """
        Local definition evaluation
        """
        new_env = env.new_environment()
        for definition in local_node.definitions:
            definition.accept(self, new_env)
        return local_node.body.accept(self, new_env)
