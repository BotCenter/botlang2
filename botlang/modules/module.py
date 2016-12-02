from botlang import BotlangSystem
from botlang import Evaluator
from botlang.evaluation.values import Nil


class Module(object):

    def __init__(self, name, body_ast):

        self.name = name
        self.body_ast = body_ast
        self.evaluated = False
        self.bindings = {}

    def get_bindings(self, module_resolver):

        if not self.evaluated:
            self.evaluate_module_code(module_resolver)
            self.evaluated = True
        return self.bindings

    def evaluate_module_code(self, module_resolver):
        """
        Evaluate the module to get the bindings it exports.
        We use a fresh environment for each module's evaluation.
        """
        environment = BotlangSystem.base_environment()
        module_evaluator = ModuleEvaluator(module_resolver, self)
        self.body_ast.accept(module_evaluator, environment)

    def add_binding(self, id, closure):

        self.bindings[id] = closure


class ModuleEvaluator(Evaluator):
    """
    AST visitor for module evaluation
    """
    def __init__(self, module_resolver, module):

        super(ModuleEvaluator, self).__init__(module_resolver=module_resolver)
        self.module = module

    def visit_module_function_export(self, provide_node, env):

        self.execution_stack.append(provide_node)
        value = provide_node.identifier_to_export.accept(
            self.get_evaluator(),
            env
        )
        self.module.add_binding(
            provide_node.identifier_to_export.identifier,
            value
        )
        self.execution_stack.pop()
        return Nil

    def get_evaluator(self):

        evaluator = Evaluator(module_resolver=self.module_resolver)
        evaluator.execution_stack = self.execution_stack
        return evaluator
