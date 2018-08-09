from functools import reduce
from botlang.ast.ast_visitor import ASTVisitor
from botlang.evaluation.oop import OopHelper
from botlang.evaluation.values import *


class ExecutionStack(list):

    def print_trace(self):

        from botlang.macros.default_macros import DefaultMacros
        return reduce(
            lambda a, n: a + n + '\n',
            [
                self.frame_message(frame) for frame in self
                if frame.s_expr.source_reference.source_id !=
                DefaultMacros.DEFAULT_MACROS_SOURCE_ID
            ],
            ''
        )

    @classmethod
    def frame_message(cls, frame):

        return '\tModule "{0}", line {1}, in {2}:\n\t\t{3}'.format(
            frame.s_expr.source_reference.source_id,
            frame.s_expr.source_reference.start_line,
            frame.print_node_type(),
            frame.s_expr.code.split('\n')[0]
        )


class Evaluator(ASTVisitor):
    """
    AST visitor for evaluation
    """
    def __init__(self, module_resolver=None):

        if module_resolver is None:
            raise Exception('Module resolver required')
        self.module_resolver = module_resolver
        self.execution_stack = ExecutionStack()

    def visit_val(self, val_node, env):
        """
        Value expression evaluation
        """
        return val_node.value

    def visit_list(self, literal_list, env):
        return [
            element.accept(self, env) for element in literal_list.elements
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

    def visit_class_definition(self, class_node, env):

        self.execution_stack.append(class_node)
        superclass_obj = OopHelper.class_lookup(class_node.superclass, env)
        methods = {
            member.identifier: member.definition.accept(self, env)
            for member in class_node.methods
        }
        attributes = {
            attr.identifier: attr.definition.accept(self, env)
            if attr.definition else Nil
            for attr in class_node.attributes
        }
        class_obj = OopHelper.build_class(
            class_node.name,
            superclass_obj,
            attributes,
            methods
        )
        env.update(
            {class_node.name: class_obj}
        )
        self.execution_stack.pop()

    def visit_and(self, and_node, env):
        """
        Logical 'and' evaluation
        """
        self.execution_stack.append(and_node)
        left_branch = and_node.cond1.accept(self, env)
        result = left_branch and and_node.cond2.accept(self, env)
        self.execution_stack.pop()
        return result

    def visit_or(self, or_node, env):
        """
        Logical 'or' evaluation
        """
        self.execution_stack.append(or_node)
        left_branch = or_node.cond1.accept(self, env)
        result = left_branch or or_node.cond2.accept(self, env)
        self.execution_stack.pop()
        return result

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
        """
        self.execution_stack.append(bot_result_node)
        data = bot_result_node.data.accept(self, env)
        message = bot_result_node.message.accept(self, env)
        next_node = bot_result_node.next_node.accept(self, env)

        bot_result_value = BotResultValue(
            data,
            message,
            next_node
        )
        self.execution_stack.pop()
        return bot_result_value

    def visit_app(self, app_node, env):
        """
        Function application evaluation.
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
        if fun_val.is_reflective():
            result = fun_val.apply(env, *arg_vals)
        else:
            result = fun_val.apply(*arg_vals)
        self.execution_stack.pop()
        return result

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
        from botlang.modules.module import BotlangModule
        module = BotlangModule(
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
        bindings = self.module_resolver.get_bindings(self, module_name)
        env.update(bindings)
        self.execution_stack.pop()
        return Nil


class NotInModuleContextException(Exception):

    def __init__(self):
        super(NotInModuleContextException, self).__init__(
            'The "provide" keyword must appear in a top-level module context'
        )
