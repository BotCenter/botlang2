from botlang.ast.ast_visitor import ASTVisitor
from botlang.evaluation.values import Nil, Primitive


class Module(object):

    def __init__(self, name):
        self.name = name

    def get_bindings(self, evaluator):
        raise NotImplementedError


class BotlangModule(Module):

    def __init__(self, name, body_ast):

        super(BotlangModule, self).__init__(name)
        self.body_ast = body_ast
        self.evaluated = False
        self.bindings = {}

    def get_bindings(self, evaluator):

        if not self.evaluated:
            self.evaluate_module_code(evaluator)
            self.evaluated = True
        return self.bindings

    def evaluate_module_code(self, evaluator):

        module_evaluator = ModuleEvaluator(evaluator, self)
        self.body_ast.accept(
            module_evaluator,
            evaluator.module_resolver.environment
        )

    def add_binding(self, id, closure):

        self.bindings[id] = closure


class ExternalModule(Module):

    def __init__(self, name, function_bindings):

        super(ExternalModule, self).__init__(name)
        self.function_bindings = function_bindings

    def get_bindings(self, evaluator):

        return {
            key: Primitive(primitive, None)
            for key, primitive in self.function_bindings.items()
        }


class ModuleEvaluator(ASTVisitor):
    """
    AST visitor for module evaluation
    """
    def __init__(self, evaluator, module):

        self.evaluator = evaluator
        self.module = module
        self.body_count = 0

    def visit_module_function_export(self, provide_node, env):

        self.evaluator.execution_stack.append(provide_node)

        for identifier in provide_node.identifiers_to_export:
            value = identifier.accept(self.evaluator, env)
            self.module.add_binding(identifier.identifier, value)

        self.evaluator.execution_stack.pop()
        return Nil

    def visit_body(self, body_node, env):

        evaluator = self if self.body_count == 0 else self.evaluator
        self.body_count += 1

        self.evaluator.execution_stack.append(body_node)
        for expr in body_node.expressions[0:-1]:
            expr.accept(evaluator, env)
        result = body_node.expressions[-1].accept(evaluator, env)
        self.evaluator.execution_stack.pop()
        return result

    def visit_cond(self, cond_node, env):
        return self.evaluator.visit_cond(cond_node, env)

    def visit_module_definition(self, module_node, env):
        return self.evaluator.visit_module_definition(module_node, env)

    def visit_module_import(self, require_node, env):
        return self.evaluator.visit_module_import(require_node, env)

    def visit_and(self, and_node, env):
        return self.evaluator.visit_and(and_node, env)

    def visit_or(self, or_node, env):
        return self.evaluator.visit_or(or_node, env)

    def visit_app(self, app_node, env):
        return self.evaluator.visit_app(app_node, env)

    def visit_cond_else_clause(self, else_node, env):
        return self.evaluator.visit_cond_else_clause(else_node, env)

    def visit_cond_predicate_clause(self, predicate_node, env):
        return self.evaluator.visit_cond_predicate_clause(predicate_node, env)

    def visit_definition(self, def_node, env):
        return self.evaluator.visit_definition(def_node, env)

    def visit_fun(self, fun_node, env):
        return self.evaluator.visit_fun(fun_node, env)

    def visit_id(self, id_node, env):
        return self.evaluator.visit_id(id_node, env)

    def visit_if(self, if_node, env):
        return self.evaluator.visit_if(if_node, env)

    def visit_local(self, local_node, env):
        return self.evaluator.visit_local(local_node, env)

    def visit_val(self, val_node, env):
        return self.evaluator.visit_val(val_node, env)
