import typing
import runtime.values as Value
import parser.nodes as Nodes
from runtime.env import Env
from backend import errors

# TODO Give a proper name to this shit
class FnContainerThingy(typing.NamedTuple):
    package: str
    fn: str
    args: typing.Optional[tuple] = None

dct: typing.Dict[Nodes.AllStmtsTypeHint, FnContainerThingy] = {
    Nodes.IdentifierNode: FnContainerThingy("exprs", "eval_identifier"),
    Nodes.IntNode: FnContainerThingy("Value", "Int"),
    Nodes.FloatNode: FnContainerThingy("Value", "Float"),
    Nodes.NullNode: FnContainerThingy("Value", "Null", ()),
    Nodes.StrNode: FnContainerThingy("Value", "Str"),
    Nodes.BoolNode: FnContainerThingy("Value", "Bool"),

    Nodes.ConditionalNode: FnContainerThingy("stmts", "eval_conditional"),
    Nodes.WhileLoopNode: FnContainerThingy("stmts", "eval_while_loop"),
    Nodes.GlorifiedWhileLoopNode: FnContainerThingy("smts", "eval_glorified_while_loop"),
    Nodes.BreakNode: FnContainerThingy("stmts", "eval_break"),
    Nodes.ContinueNode: FnContainerThingy("stmts", "eval_continue"),
    Nodes.ScopeBlock: FnContainerThingy("stmts", "eval_scope_block"),
    Nodes.SubscriptionNode: FnContainerThingy("exprs", "eval_subscription"),
    Nodes.MemberAccessNode: FnContainerThingy("exprs", "eval_member_access"),
    Nodes.UnaryNode: FnContainerThingy("exprs", "eval_unary"),
    Nodes.WalrusNode: FnContainerThingy("exprs", "eval_walrus"),
    Nodes.BinaryNode: FnContainerThingy("exprs", "eval_binary_expr"),
    Nodes.ComparisonNode: FnContainerThingy("exprs", "eval_comparison_expr"),
    Nodes.TernaryNode: FnContainerThingy("exprs", "eval_ternary_expr"),
    Nodes.CallNode: FnContainerThingy("exprs", "eval_call_expr"),
    Nodes.AssignmentNode: FnContainerThingy("stmts", "eval_assignment"),
    Nodes.VarDeclarationNode: FnContainerThingy("stmts", "eval_var_declaration"),
    Nodes.ModifierAssignmentNode: FnContainerThingy("stmts", "eval_modifier_assignment"),
    Nodes.ProgramNode: FnContainerThingy("stmts", "eval_program")
}

def evaluate(node: Nodes.Stmt, env: Env) -> Value.RuntimeVal:
    import runtime.eval.exprs as exprs
    import runtime.eval.stmts as stmts
    
    try:
        for node_class, ct in dct.items():
            # ^ Special cases
            # ? Code block
            if node_class == Nodes.CodeBlock and isinstance(node, Nodes.CodeBlock):
                code_block_env = Env(env)
                val = exprs.eval_code_block(node, code_block_env)
                del code_block_env
                return val
            
            # ^ Normal cases
            
            if isinstance(node, node_class):
                ## A primitive value
                if ct.package == "Value":
                    if ct.args is None:
                        return getattr(Value, ct.fn)(node.value)
                    return getattr(Value, ct.fn)(*ct.args)
                
                return getattr(eval(ct.package), ct.fn)(node, env)
    except errors.BreakLoop:
        raise errors.SyntaxError("'break' run outside of a loop")
    except errors.ContinueLoop:
        raise errors.SyntaxError("'continue' run outside of a loop")
    except errors.ReturnValue:
        raise errors.SyntaxError("'return' run outside of a function")

    # $ If the code reaches here, it means that there's an invalid node in the AST
    # $ that the interperter couldn't identify, which should never happened
    # ! Throw an error to signify
    raise errors.InternalError(f"Unable to parse AST node {node}")