import typing
import runtime.values as Value
import parser.nodes as Nodes
from runtime.env import Env

# TODO Give a proper name
class FnContainerThingy(typing.NamedTuple):
    fn: typing.Callable
    args: typing.Optional[tuple] = None # None will be replaced by (node, env)

def evaluate(node: Nodes.Stmt, env: Env) -> Value.RuntimeVal:
    import runtime.eval.exprs as exprs
    import runtime.eval.stmts as stmts
    
    dct: typing.Dict[Nodes.AllStmtsTypeHint, FnContainerThingy] = {
        Nodes.Identifier: FnContainerThingy(exprs.eval_identifier),
        Nodes.Int: FnContainerThingy(Value.Int, ("value",)),
        Nodes.Float: FnContainerThingy(Value.Float, ("value",)),
        Nodes.Null: FnContainerThingy(Value.Null, ()),
        Nodes.Str: FnContainerThingy(Value.Str, ("value",)),
        Nodes.Bool: FnContainerThingy(Value.Bool, ("value",)),
        Nodes.Conditional: FnContainerThingy(stmts.eval_conditional),
        Nodes.WhileLoop: FnContainerThingy(stmts.eval_while_loop),
        # Nodes.Subscription: FnContainerThingy(exprs.eval_subscription),
        # Nodes.MemberAccess: FnContainerThingy(exprs.eval_member_access),
        Nodes.Unary: FnContainerThingy(exprs.eval_unary),
        Nodes.Walrus: FnContainerThingy(exprs.eval_walrus),
        Nodes.CodeBlock: None, # Handle separately by the code
        Nodes.Binary: FnContainerThingy(exprs.eval_binary_expr),
        Nodes.Comparison: FnContainerThingy(exprs.eval_comparison_expr),
        Nodes.Ternary: FnContainerThingy(exprs.eval_ternary_expr),
        Nodes.Call: FnContainerThingy(exprs.eval_call_expr),
        Nodes.Assignment: FnContainerThingy(stmts.eval_assignment),
        Nodes.VarDeclaration: FnContainerThingy(stmts.eval_var_declaration),
        Nodes.ModifierAssignment: FnContainerThingy(stmts.eval_modifier_assignment),
        Nodes.Program: FnContainerThingy(stmts.eval_program)
    }
    
    for node_class, i in dct.items():
        # Special cases
        if node_class == Nodes.CodeBlock and isinstance(node, Nodes.CodeBlock):
            code_block_env = Env(env)
            return exprs.eval_code_block(node, code_block_env)
        if isinstance(node, node_class):
            if i.args is None:
                return i.fn(node, env)
            return i.fn(*(getattr(node, arg) for arg in i.args))
    
    # match node.kind:
    #     # ^ Primary Expressions
    #     case NodeType.Identifier:
    #         return exprs.eval_identifier(node, env)
    #     case NodeType.Int:
    #         return Value.Int(node.value)
    #     case NodeType.Float:
    #         return Value.Float(node.value)
    #     case NodeType.Str:
    #         return Value.Str(node.value)
    #     case NodeType.Bool:
    #         return Value.Bool(node.value)
    #     case NodeType.Null:
    #         return Value.Null()
        
    #     # ^ Expressions
    #     case NodeType.Conditional:
    #         return exprs.eval_conditional(node, env)
    #     case NodeType.Subscription:
    #         return exprs.eval_subscription(node, env)
    #     case NodeType.MemberAccess:
    #         return exprs.eval_member_access(node, env)
    #     case NodeType.Unary:
    #         return exprs.eval_unary(node, env)
    #     case NodeType.Walrus:
    #         return exprs.eval_walrus(node, env)
    #     case NodeType.CodeBlock:
    #         code_block_env = Env(env)
    #         return exprs.eval_code_block(node, code_block_env)
    #     case NodeType.Binary:
    #         return exprs.eval_binary_expr(node, env)
    #     case NodeType.Comparison:
    #         return exprs.eval_comparison_expr(node, env)
    #     case NodeType.Ternary:
    #         return exprs.eval_ternary_expr(node, env)
    #     case NodeType.Call:
    #         return exprs.eval_call_expr(node, env)
        
    #     # ^ Statements
    #     case NodeType.Assignment:
    #         stmts.eval_assignment(node, env)
    #     case NodeType.VarDeclaration:
    #         stmts.eval_var_declaration(node, env)
    #     case NodeType.ModifierAssignment:
    #         stmts.eval_modifier_assignment(node, env)
    #     case NodeType.Program:
    #         stmts.eval_program(node, env)
    #     case _:
    #         raise Exception(node)