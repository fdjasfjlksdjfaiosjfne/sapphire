import typing
import runtime.values as Value
import parser.nodes as Nodes
from runtime.env import Env
import types

# TODO Give a proper name to this shit
class FnContainerThingy(typing.NamedTuple):
    package: str
    fn: str
    args: typing.Optional[tuple] = None

dct: typing.Dict[Nodes.AllStmtsTypeHint, FnContainerThingy] = {
    Nodes.Identifier: FnContainerThingy("exprs", "eval_identifier"),
    Nodes.Int: FnContainerThingy("Value", "Int"),
    Nodes.Float: FnContainerThingy("Value", "Float"),
    Nodes.Null: FnContainerThingy("Value", "Null", ()),
    Nodes.Str: FnContainerThingy("Value", "Str"),
    Nodes.Bool: FnContainerThingy("Value", "Bool"),
    Nodes.Conditional: FnContainerThingy("stmts", "eval_conditional"),
    Nodes.WhileLoop: FnContainerThingy("stmts", "eval_while_loop"),
    Nodes.Subscription: FnContainerThingy("exprs", "eval_subscription"),
    Nodes.MemberAccess: FnContainerThingy("exprs", "eval_member_access"),
    Nodes.Unary: FnContainerThingy("exprs", "eval_unary"),
    Nodes.Walrus: FnContainerThingy("exprs", "eval_walrus"),
    Nodes.Binary: FnContainerThingy("exprs", "eval_binary_expr"),
    Nodes.Comparison: FnContainerThingy("exprs", "eval_comparison_expr"),
    Nodes.Ternary: FnContainerThingy("exprs", "eval_ternary_expr"),
    Nodes.Call: FnContainerThingy("exprs", "eval_call_expr"),
    Nodes.Assignment: FnContainerThingy("stmts", "eval_assignment"),
    Nodes.VarDeclaration: FnContainerThingy("stmts", "eval_var_declaration"),
    Nodes.ModifierAssignment: FnContainerThingy("stmts", "eval_modifier_assignment"),
    Nodes.Program: FnContainerThingy("stmts", "eval_program")
}

def evaluate(node: Nodes.Stmt, env: Env) -> Value.RuntimeVal:
    import runtime.eval.exprs as exprs
    import runtime.eval.stmts as stmts
    
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
    
    # $ If the code reaches here, it means that there's an invalid node in the AST
    # $ that the interperter couldn't identify, which should never happened
    # ! Throw an error to signify
    raise Exception()

