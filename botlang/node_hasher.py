import base64
import hashlib

from botlang.ast.visitor import Visitor


class NodeHasher(Visitor):
    """
    AST visitor for adding nodes to a dictionary with a unique and
    deterministic key.
    """
    def __init__(self):
        self.ast_nodes = {}

    def visit_val(self, val_node, env):

        return self.hash_and_store(str(val_node.value), val_node)

    def visit_if(self, if_node, env):

        cond_hash = if_node.cond.accept(self, env)
        true_hash = if_node.if_true.accept(self, env)
        false_hash = if_node.if_false.accept(self, env)
        return self.hash_and_store(
            cond_hash + true_hash + false_hash,
            if_node
        )

    def visit_and(self, and_node, env):

        cond1_hash = and_node.cond1.accept(self, env)
        cond2_hash = and_node.cond2.accept(self, env)
        return self.hash_and_store(cond1_hash + cond2_hash, and_node)

    def visit_or(self, or_node, env):

        cond1_hash = or_node.cond1.accept(self, env)
        cond2_hash = or_node.cond2.accept(self, env)
        return self.hash_and_store(cond1_hash + cond2_hash, or_node)

    def visit_id(self, id_node, env):

        return self.hash_and_store(id_node.identifier, id_node)

    def visit_fun(self, fun_node, env):

        hash_val = self.hash_function_node(fun_node.params, fun_node.body)
        fun_node.node_id = hash_val
        self.ast_nodes[hash_val] = fun_node
        return hash_val

    def visit_bot_node(self, bot_node, env):

        hash_val = self.hash_function_node(bot_node.params, bot_node.body)
        bot_node.node_id = hash_val
        self.ast_nodes[hash_val] = bot_node
        return hash_val

    def visit_bot_result(self, bot_result, env):

        data_hash = bot_result.data.accept(self, env)
        message_hash = bot_result.message.accept(self, env)
        next_node_hash = bot_result.next_node.accept(self, env)
        return self.hash_and_store(
            data_hash + message_hash + next_node_hash,
            bot_result
        )

    def visit_app(self, app_node, env):

        fun_hash = app_node.fun_expr.accept(self, env)
        arg_hashes = [arg.accept(self, env) for arg in app_node.arg_exprs]
        args_hash = reduce(str.__add__, arg_hashes, '') if arg_hashes else ''
        return self.hash_and_store(fun_hash + args_hash, app_node)

    def visit_body(self, body_node, env):

        expr_hashes = [
            expr.accept(self, env) for expr in body_node.expressions[0:]]
        return self.hash_and_store(
            reduce(str.__add__, expr_hashes, ''),
            body_node
        )

    def visit_definition(self, def_node, env):

        return self.hash_and_store(
            def_node.name + def_node.expr.accept(self, env),
            def_node
        )

    def visit_local(self, local_node, env):

        def_hashes = [
            definition.accept(self, env) for definition
            in local_node.definitions
            ]
        return self.hash_and_store(
            reduce(str.__add__, def_hashes, ''),
            local_node
        )

    def hash_and_store(self, string, node):

        hash_val = self.hash_function(string)
        node.node_id = hash_val
        self.ast_nodes[hash_val] = node
        return hash_val

    def hash_function_node(self, params, body):

        params_str = reduce(str.__add__, params, '') if params else ''
        body_hash = body.accept(self, None)
        return self.hash_function(params_str + body_hash)

    @classmethod
    def hash_function(cls, string):
        return base64.b64encode(hashlib.md5(string).hexdigest())
