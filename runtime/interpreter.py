import typing
import runtime.values as values
import parser.nodes as Nodes
from runtime.env import Env
from backend import errors


class ExprEvalHandler(typing.NamedTuple):
    function_name: str
    def __call__(self, node, env):
        from runtime.eval import exprs
        return getattr(exprs, self.function_name)(node, env)

class StmtEvalHandler(typing.NamedTuple):
    function_name: str
    def __call__(self, node, env):
        from runtime.eval import stmts
        return getattr(stmts, self.function_name)(node, env)

class ValueEvalHandler(typing.NamedTuple):
    function_name: str
    def __call__(self, *args, **kwargs):
        return getattr(values, self.function_name)(*args, **kwargs)

eval_registry: dict[type[Nodes.StmtNode], ExprEvalHandler | StmtEvalHandler | ValueEvalHandler] = {
    Nodes.IdentifierNode: ExprEvalHandler("eval_identifier"),
    Nodes.IntNode: ValueEvalHandler("Int"),
    Nodes.FloatNode: ValueEvalHandler("Float"),
    Nodes.NullNode: ValueEvalHandler("Null"),
    Nodes.StrNode: ValueEvalHandler("Str"),
    Nodes.BoolNode: ValueEvalHandler("Bool"),
    Nodes.ListNode: ValueEvalHandler("List"),
    Nodes.TupleNode: ValueEvalHandler("Tuple"),
    Nodes.SetNode: ValueEvalHandler("Set"),
    Nodes.ConditionalNode: StmtEvalHandler("eval_conditional"),
    Nodes.WhileLoopNode: StmtEvalHandler("eval_while_loop"),
    Nodes.GlorifiedWhileLoopNode: StmtEvalHandler("eval_glorified_while_loop"),
    Nodes.BreakNode: StmtEvalHandler("eval_break"),
    Nodes.ContinueNode: StmtEvalHandler("eval_continue"),
    Nodes.ScopeBlockNode: StmtEvalHandler("eval_scope_block"),
    Nodes.SubscriptionNode: ExprEvalHandler("eval_subscription"),
    Nodes.AttributeNode: ExprEvalHandler("eval_member_access"),
    Nodes.UnaryNode: ExprEvalHandler("eval_unary"),
    Nodes.WalrusNode: ExprEvalHandler("eval_walrus"),
    Nodes.BinaryNode: ExprEvalHandler("eval_binary_expr"),
    Nodes.ComparisonNode: ExprEvalHandler("eval_comparison_expr"),
    Nodes.TernaryNode: ExprEvalHandler("eval_ternary_expr"),
    Nodes.CallNode: ExprEvalHandler("eval_call_expr"),
    Nodes.AssignmentNode: ExprEvalHandler("eval_assignment"),
    Nodes.VarDeclarationNode: StmtEvalHandler("eval_var_declaration"),
    Nodes.ModifierAssignmentNode: StmtEvalHandler( "eval_modifier_assignment"),
    Nodes.ModuleNode: StmtEvalHandler("eval_program")
}

def evaluate(node: Nodes.BaseNode, env: Env) -> values.RuntimeVal:
    try:
        for node_class, handler in eval_registry.items():
            if not isinstance(node, node_class):
                continue
            if isinstance(handler, (StmtEvalHandler, ExprEvalHandler)):
                handler(node, env)
            elif isinstance(handler, ValueEvalHandler):
                if isinstance(node, Nodes.LiteralNode):
                    handler(node.value)
                else:
                    raise errors.InternalError()

    except errors.BreakLoop:
        raise errors.SyntaxError("'break' run outside of a loop")
    except errors.ContinueLoop:
        raise errors.SyntaxError("'continue' run outside of a loop")
    except errors.ReturnValue:
        raise errors.SyntaxError("'return' run outside of a function")


    # $ If the code reaches here, it means that there's an invalid node in the AST
    # $ that the interperter couldn't identify, which should never happened
    # ! Throw an InternalError to signify
    raise errors.InternalError(
        f"No evaluator registered for AST node: {type(node).__name__}"
    )