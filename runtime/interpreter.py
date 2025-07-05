import typing
import runtime.values as values
import parser.nodes as Nodes
from runtime.env import Env
from backend import errors

# TODO Give a proper name to this shit
class EvaluationHandler(typing.NamedTuple):
    package: str
    fn: str
    static_args: typing.Optional[tuple] = None

eval_registry: dict[type[Nodes.StmtNode], EvaluationHandler] = {
    Nodes.IdentifierNode: EvaluationHandler("exprs", "eval_identifier"),
    Nodes.IntNode: EvaluationHandler("Value", "Int"),
    Nodes.FloatNode: EvaluationHandler("Value", "Float"),
    Nodes.NullNode: EvaluationHandler("Value", "Null", ()),
    Nodes.StrNode: EvaluationHandler("Value", "Str"),
    Nodes.BoolNode: EvaluationHandler("Value", "Bool"),
    Nodes.ListNode: EvaluationHandler("Value", "List"),
    Nodes.ConditionalNode: EvaluationHandler("stmts", "eval_conditional"),
    Nodes.WhileLoopNode: EvaluationHandler("stmts", "eval_while_loop"),
    Nodes.GlorifiedWhileLoopNode: EvaluationHandler("smts", "eval_glorified_while_loop"),
    Nodes.BreakNode: EvaluationHandler("stmts", "eval_break"),
    Nodes.ContinueNode: EvaluationHandler("stmts", "eval_continue"),
    Nodes.ScopeBlockNode: EvaluationHandler("stmts", "eval_scope_block"),
    Nodes.SubscriptionNode: EvaluationHandler("exprs", "eval_subscription"),
    Nodes.MemberAccessNode: EvaluationHandler("exprs", "eval_member_access"),
    Nodes.UnaryNode: EvaluationHandler("exprs", "eval_unary"),
    Nodes.WalrusNode: EvaluationHandler("exprs", "eval_walrus"),
    Nodes.BinaryNode: EvaluationHandler("exprs", "eval_binary_expr"),
    Nodes.ComparisonNode: EvaluationHandler("exprs", "eval_comparison_expr"),
    Nodes.TernaryNode: EvaluationHandler("exprs", "eval_ternary_expr"),
    Nodes.CallNode: EvaluationHandler("exprs", "eval_call_expr"),
    Nodes.AssignmentNode: EvaluationHandler("stmts", "eval_assignment"),
    Nodes.VarDeclarationNode: EvaluationHandler("stmts", "eval_var_declaration"),
    Nodes.ModifierAssignmentNode: EvaluationHandler("stmts", "eval_modifier_assignment"),
    Nodes.ProgramNode: EvaluationHandler("stmts", "eval_program")
}

def evaluate(node: Nodes.StmtNode, env: Env) -> values.RuntimeVal:
    import runtime.eval.exprs as exprs
    import runtime.eval.stmts as stmts

    try:
        for node_class, handler in eval_registry.items():
            if not isinstance(node, node_class):
                continue

            if handler.package == "Value":
                return getattr(values, handler.function_name)(*(node.value,) if handler.static_args is None else handler.static_args)

            # Dynamic import routing (if you want to avoid fixed `import` above)
            mod = {"exprs": exprs, "stmts": stmts}[handler.package]
            return getattr(mod, handler.function_name)(node, env)

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