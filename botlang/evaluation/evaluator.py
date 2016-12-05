from functools import reduce
from botlang.ast.visitor import Visitor
from botlang.evaluation.values import *


class ExecutionState(object):

    def __init__(self, primitives_values, bot_node_steps):

        self.primitives_values = primitives_values
        self.bot_node_steps = bot_node_steps


class ExecutionStack(list):

    def print_trace(self):

        return reduce(
            lambda a, n: a + n + '\n',
            [self.frame_message(frame) for frame in self],
            ''
        )

    @classmethod
    def frame_message(cls, frame):

        return '\tFile "{0}", line {1}, in\n\t\t{2}'.format(
            frame.s_expr.source_reference.source_id,
            frame.s_expr.source_reference.start_line,
            frame.s_expr.code.split('\n')[0]
        )


class Evaluator(Visitor):
    """
    AST visitor for evaluation
    """
    def __init__(self, evaluation_state=None, module_resolver=None):

        if module_resolver is None:
            from botlang.modules.resolver import ModuleResolver
            module_resolver = ModuleResolver()
        self.module_resolver = module_resolver

        if evaluation_state is not None:
            self.primitives_evaluations = evaluation_state.primitives_values[:]
            self.bot_result_skips = evaluation_state.bot_node_steps
        else:
            self.primitives_evaluations = []
            self.bot_result_skips = 0

        self.primitive_step = 0
        self.bot_node_step = 0
        self.execution_stack = ExecutionStack()

    def visit_val(self, val_node, env):
        """
        Value expression evaluation
        """
        return val_node.value

    def visit_list(self, list_node, env):
        """
        List expression evaluation
        """
        return [
            element.accept(self, env) for element in list_node.elements
        ]

    def visit_if(self, if_node, env):
        """
        'If' construct evaluation
        """
        self.execution_stack.append(if_node)

        if if_node.cond.accept(self, env):
            self.execution_stack.pop()
            return if_node.if_true.accept(self, env)
        else:
            self.execution_stack.pop()
            return if_node.if_false.accept(self, env)

    def visit_cond(self, cond_node, env):
        """
        'Cond' conditional evaluation
        """
        self.execution_stack.append(cond_node)

        value = None
        for clause in cond_node.cond_clauses:
            value = clause.accept(self, env)
            if value is not None:
                break

        self.execution_stack.pop()
        return value

    def visit_cond_predicate_clause(self, predicate_node, env):
        """
        'Cond' predicate clause evaluation
        """
        self.execution_stack.append(predicate_node)
        value = None
        if predicate_node.predicate.accept(self, env):
            value = predicate_node.then_body.accept(self, env)
        self.execution_stack.pop()
        return value

    def visit_cond_else_clause(self, else_node, env):
        """
        'Cond' else clause evaluation
        """
        self.execution_stack.append(else_node)
        value = else_node.then_body.accept(self, env)
        self.execution_stack.pop()
        return value

    def visit_and(self, and_node, env):
        """
        Logical 'and' evaluation
        """
        self.execution_stack.append(and_node)
        left_branch = and_node.cond1.accept(self, env)
        right_branch = and_node.cond2.accept(self, env)

        self.execution_stack.pop()
        return left_branch and right_branch

    def visit_or(self, or_node, env):
        """
        Logical 'or' evaluation
        """
        self.execution_stack.append(or_node)
        left_branch = or_node.cond1.accept(self, env)
        right_branch = or_node.cond2.accept(self, env)

        self.execution_stack.pop()
        return left_branch or right_branch

    def visit_id(self, id_node, env):
        """
        Identifier (variable name) resolution
        """
        self.execution_stack.append(id_node)
        identifier = env.lookup(id_node.identifier)
        self.execution_stack.pop()
        return identifier

    def visit_fun(self, fun_node, env):
        """
        Function expression evaluation.
        Returns closure
        """
        self.execution_stack.append(fun_node)
        closure = Closure(fun_node, env, self)
        self.execution_stack.pop()
        return closure

    def visit_bot_node(self, bot_node, env):
        """
        Bot node expression evaluation.
        Returns bot-node closure
        """
        self.execution_stack.append(bot_node)
        bot_node = BotNodeValue(bot_node, env, self)
        self.execution_stack.pop()
        return bot_node

    def visit_bot_result(self, bot_result_node, env):
        """
        Bot result evaluation. Returns a BotResultValue which can be used
        to resume execution in the future.

        If the bot_result_skips number configured for this evaluator is
        greater or equal than the current bot_node_step, instead of returning
        a BotResultValue the next node is evaluated immediately.
        """
        self.execution_stack.append(bot_result_node)
        data = bot_result_node.data.accept(self, env)
        message = bot_result_node.message.accept(self, env)
        next_node = bot_result_node.next_node.accept(self, env)
        self.bot_node_step += 1

        if self.bot_node_step <= self.bot_result_skips:
            next_node_value = next_node.apply(data)
            self.execution_stack.pop()
            return next_node_value
        else:
            evaluation_state = ExecutionState(
                self.primitives_evaluations,
                self.bot_node_step
            )
            bot_result_value = BotResultValue(
                data,
                message,
                next_node,
                evaluation_state
            )
            self.execution_stack.pop()
            return bot_result_value

    def visit_app(self, app_node, env):
        """
        Function application evaluation. If the function being applied is a
        primitive we check if its value is already stored in this evaluator.
        If it's not, then the value is computed and stored in the
        primitives_evaluation list.
        """
        self.execution_stack.append(app_node)
        fun_val = app_node.fun_expr.accept(self, env)
        if not isinstance(fun_val, FunVal):
            raise Exception(
                'Invalid function application: {0} is not a function'.format(
                    fun_val
                )
            )

        arg_vals = [arg.accept(self, env) for arg in app_node.arg_exprs]

        if fun_val.must_be_cached():
            if self.primitive_step == len(self.primitives_evaluations):
                return_value = fun_val.apply(*arg_vals)
                self.primitives_evaluations.append(return_value)
                self.primitive_step += 1
                self.execution_stack.pop()
                return return_value
            else:
                return_value = self.primitives_evaluations[self.primitive_step]
                self.primitive_step += 1
                self.execution_stack.pop()
                return return_value

        self.execution_stack.pop()
        return fun_val.apply(*arg_vals)

    def visit_body(self, body_node, env):
        """
        Evaluation of a sequence of expressions
        """
        self.execution_stack.append(body_node)
        for expr in body_node.expressions[0:-1]:
            expr.accept(self, env)
        result = body_node.expressions[-1].accept(self, env)
        self.execution_stack.pop()
        return result

    def visit_definition(self, def_node, env):
        """
        Definition evaluation.

        Mutates the environment with this definition.
        Evaluates the definition body with the same environment
        that is mutated, which allows recursion.
        Doesn't return a value.
        """
        self.execution_stack.append(def_node)
        env.update(
            {def_node.name: def_node.expr.accept(self, env)}
        )
        self.execution_stack.pop()

    def visit_local(self, local_node, env):
        """
        Local definition evaluation
        """
        self.execution_stack.append(local_node)
        new_env = env.new_environment()
        for definition in local_node.definitions:
            definition.accept(self, new_env)
        result = local_node.body.accept(self, new_env)

        self.execution_stack.pop()
        return result

    def visit_module_definition(self, module_node, env):
        """
        Module definition
        """
        self.execution_stack.append(module_node)
        from botlang.modules.module import Module
        module = Module(
            module_node.name.accept(self, env),
            module_node.body
        )
        self.module_resolver.add_module(module)
        self.execution_stack.pop()
        return module

    def visit_module_function_export(self, provide_node, env):
        """
        Module function's export
        """
        raise NotInModuleContextException()

    def visit_module_import(self, require_node, env):
        """
        Import a module into scope
        """
        self.execution_stack.append(require_node)
        module_name = require_node.module_name.accept(self, env)
        bindings = self.module_resolver.get_bindings(module_name)
        env.update(bindings)
        self.execution_stack.pop()
        return Nil


class NotInModuleContextException(Exception):

    def __init__(self):
        super(NotInModuleContextException, self).__init__(
            'The "provide" keyword must appear in a top-level module context'
        )
