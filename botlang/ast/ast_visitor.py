from botlang.ast import *
from botlang.ast import ClassDefinition, MethodDefinition, \
    AttributeDefinition, BotSlotsNode, SlotDefinition, SlotsNodeBody


class ASTVisitor(object):
    """
    AST visitor base class.
    
    This default implementation provides a simple mechanism to transform an AST
    by overriding this class' methods.
    """

    def visit_val(self, val_node, env):
        """
        :param val_node: ast.Val 
        :param env: Environment
        """
        return val_node

    def visit_list(self, literal_list, env):
        """
        :param literal_list: ast.ListVal
        :param env: Environment
        """
        return ListVal([
            element.accept(self, env) for element in literal_list.elements
        ]).add_code_reference(literal_list.s_expr)

    def visit_if(self, if_node, env):
        """
        :param if_node: ast.If 
        :param env: Environment
        """
        return If(
            if_node.cond.accept(self, env),
            if_node.if_true.accept(self, env),
            if_node.if_false.accept(self, env)
        ).add_code_reference(if_node.s_expr)

    def visit_cond(self, cond_node, env):
        """
        :param cond_node: ast.Cond 
        :param env: Environment
        """
        return Cond(
            [clause.accept(self, env) for clause in cond_node.cond_clauses]
        ).add_code_reference(cond_node.s_expr)

    def visit_cond_predicate_clause(self, predicate_node, env):
        """
        :param predicate_node: ast.CondPredicateClause 
        :param env: Environment
        """
        return CondPredicateClause(
            predicate_node.predicate.accept(self, env),
            predicate_node.then_body.accept(self, env)
        ).add_code_reference(predicate_node.s_expr)

    def visit_cond_else_clause(self, else_node, env):
        """
        :param else_node: ast.CondElseClause
        :param env: Environment
        :return: 
        """
        return CondElseClause(
            else_node.then_body.accept(self, env)
        ).add_code_reference(else_node.s_expr)

    def visit_and(self, and_node, env):
        """
        :param and_node: ast.And 
        :param env: Environment
        """
        return And(
            and_node.cond1.accept(self, env),
            and_node.cond2.accept(self, env)
        ).add_code_reference(and_node.s_expr)

    def visit_or(self, or_node, env):
        """
        :param or_node: ast.Or 
        :param env: Environment
        """
        return Or(
            or_node.cond1.accept(self, env),
            or_node.cond2.accept(self, env)
        ).add_code_reference(or_node.s_expr)

    def visit_id(self, id_node, env):
        """
        :param id_node: ast.Id 
        :param env: Environment
        """
        return id_node

    def visit_fun(self, fun_node, env):
        """
        :param fun_node: ast.Fun
        :param env: Environment
        """
        return Fun(
            fun_node.params,
            fun_node.body.accept(self, env)
        ).add_code_reference(fun_node.s_expr)

    def visit_bot_node(self, bot_node, env):
        """
        :param bot_node: ast.BotNode 
        :param env: Environment
        """
        return BotNode(
            bot_node.params,
            bot_node.body.accept(self, env)
        ).add_code_reference(bot_node.s_expr)

    def visit_bot_result(self, bot_result, env):
        """
        :param bot_result: ast.BotResult
        :param env: Environment 
        """
        return BotResult(
            bot_result.data.accept(self, env),
            bot_result.message.accept(self, env),
            bot_result.next_node.accept(self, env)
        ).add_code_reference(bot_result.s_expr)

    def visit_app(self, app_node, env):
        """
        :param app_node: ast.App
        :param env: Environment
        """
        return App(
            app_node.fun_expr.accept(self, env),
            [argument.accept(self, env) for argument in app_node.arg_exprs]
        ).add_code_reference(app_node.s_expr)

    def visit_body(self, body_node, env):
        """
        :param body_node: ast.BodySequence 
        :param env: Environment
        """
        return BodySequence(
            [expr.accept(self, env) for expr in body_node.expressions]
        ).add_code_reference(body_node.s_expr)

    def visit_definition(self, def_node, env):
        """
        :param def_node: ast.Definition 
        :param env: Environment
        """
        return Definition(
            def_node.name,
            def_node.expr.accept(self, env)
        ).add_code_reference(def_node.s_expr)

    def visit_local(self, local_node, env):
        """
        :param local_node: ast.Local 
        :param env: Environment
        """
        return Local(
            [defn.accept(self, env) for defn in local_node.definitions],
            local_node.body.accept(self, env)
        ).add_code_reference(local_node.s_expr)

    def visit_class_definition(self, class_node, env):
        """
        :param class_node: ast.ClassDefinition
        :param env: Environment
        """
        return ClassDefinition(
            class_node.name,
            class_node.superclass,
            [attr.accept(self, env) for attr in class_node.attributes],
            [method.accept(self, env) for method in class_node.methods],
            [attr.accept(self, env) for attr in class_node.class_attributes],
            [method.accept(self, env) for method in class_node.class_methods]
        )

    def visit_instance_attribute(self, attribute_node, env):
        """
        :param attribute_node: ast.InstanceAttributeDefinition
        :param env: Environment
        """
        definition_ast = attribute_node.definition
        return AttributeDefinition(
            attribute_node.identifier,
            definition_ast.accept(self, env) if definition_ast else None
        )

    def visit_method_definition(self, method_node, env):
        """
        :param method_node: ast.MethodDefinition
        :param env: Environment
        """
        return MethodDefinition(
            method_node.identifier,
            method_node.definition.accept(self, env)
        )

    def visit_module_definition(self, module_node, env):
        """
        :param module_node: ast.ModuleDefinition 
        :param env: Environment
        """
        return ModuleDefinition(
            module_node.name,
            module_node.body.accept(self, env)
        ).add_code_reference(module_node.s_expr)

    def visit_module_import(self, require_node, env):
        """
        :param require_node: ast.ModuleImport 
        :param env: Environment
        """
        return require_node

    def visit_module_function_export(self, provide_node, env):
        """
        :param provide_node: ast.ModuleFunctionExport 
        :param env: Environment
        """
        return provide_node

    def visit_define_syntax(self, define_syntax_node, env):
        """
        :param define_syntax_node: ast.DefineSyntax 
        :param env: Environment
        """
        return define_syntax_node

    def visit_slots_node(self, slots_node, env):
        """
        :param slots_node: ast.BotSlotsNode
        :param env: Environment
        """
        return BotSlotsNode(
            slots_node.node_name,
            slots_node.params,
            slots_node.body.accept(self, env)
        ).add_code_reference(slots_node.s_expr)

    def visit_slots_node_body(self, slots_body, env):
        """
        :param slots_body: ast.SlotsNodeBody
        :param env: Environment
        """
        return SlotsNodeBody(
            slots_body.params,
            slots_body.before.accept(self, env)
            if slots_body.before is not None else None,
            slots_body.digress.accept(self, env)
            if slots_body.digress is not None else None,
            [slot.accept(self, env) for slot in slots_body.slots],
            slots_body.then.accept(self, env)
        ).add_code_reference(slots_body.s_expr)

    def visit_slot_definition(self, slot_def, env):
        """
        :param slot_def: ast.SlotDefinition
        :param env: Environment
        """
        return SlotDefinition(
            slot_def.slot_name,
            slot_def.context,
            slot_def.match_body.accept(self, env),
            slot_def.ask_body.accept(self, env)
        ).add_code_reference(slot_def.s_expr)
