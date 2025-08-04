import typing
from runtime import values
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

eval_registry: dict[type[Nodes.BaseASTNode], ExprEvalHandler | StmtEvalHandler | ValueEvalHandler] = {
    Nodes.IdentifierNode: ExprEvalHandler("eval_identifier"),
    Nodes.IntNode: ValueEvalHandler("IntValue"),
    Nodes.FloatNode: ValueEvalHandler("FloatValue"),
    Nodes.NullNode: ValueEvalHandler("NullValue"),
    Nodes.StrNode: ValueEvalHandler("StringValue"),
    Nodes.BoolNode: ValueEvalHandler("BoolValue"),
    Nodes.ListNode: ValueEvalHandler("ListValue"),
    Nodes.TupleNode: ValueEvalHandler("TupleValue"),
    Nodes.SetNode: ValueEvalHandler("SetValue"),
    Nodes.DictNode: ValueEvalHandler("DictValue"),
    Nodes.CodeBlockNode: ExprEvalHandler("eval_code_block"),
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

def evaluate(node: Nodes.BaseASTNode, env: Env) -> values.RuntimeValue:
    for node_class, handler in eval_registry.items():
        if not isinstance(node, node_class):
            continue
        if isinstance(handler, (StmtEvalHandler, ExprEvalHandler)):
            return handler(node, env)
        elif isinstance(handler, ValueEvalHandler):
            if isinstance(node, Nodes.LiteralNode):
                return handler(node.value)
            else:
                raise errors.InternalError()

    # $ If the code reaches here, it means that there's an invalid node in the AST
    # $ that the interperter couldn't identify, which should never happened
    # ! Throw an InternalError to signify
    raise errors.InternalError(
        f"No evaluator registered for AST node: {type(node).__name__}"
    )