import runtime.values as Value
from parser.nodes import NodeType, Stmt
from runtime.env import Env

def evaluate(node: Stmt, env: Env) -> Value.RuntimeVal:
    import runtime.eval.exprs as exprs
    import runtime.eval.stmts as stmts
    match node.kind:
        # ^ Primary Expressions
        case NodeType.Identifier:
            return exprs.eval_identifier(node, env)
        case NodeType.Int:
            return Value.Int(node.value)
        case NodeType.Float:
            return Value.Float(node.value)
        case NodeType.Str:
            return Value.Str(node.value)
        case NodeType.Bool:
            return Value.Bool(node.value)
        case NodeType.Null:
            return Value.Null()
        
        # ^ Expressions
        case NodeType.Conditional:
            return exprs.eval_conditional(node, env)
        case NodeType.Subscription:
            return exprs.eval_subscription(node, env)
        case NodeType.MemberAccess:
            return exprs.eval_member_access(node, env)
        case NodeType.Unary:
            return exprs.eval_unary(node, env)
        case NodeType.WalrusExpr:
            return exprs.eval_walrus(node, env)
        case NodeType.CodeBlock:
            code_block_env = Env(env)
            return exprs.eval_code_block(node, code_block_env)
        case NodeType.BinaryExpr:
            return exprs.eval_binary_expr(node, env)
        case NodeType.Comparison:
            return exprs.eval_comparison_expr(node, env)
        case NodeType.Ternary:
            return exprs.eval_ternary_expr(node, env)
        case NodeType.Call:
            return exprs.eval_call_expr(node, env)
        
        # ^ Statements
        case NodeType.Assignment:
            stmts.eval_assignment(node, env)
        case NodeType.VarDeclaration:
            stmts.eval_var_declaration(node, env)
        case NodeType.ModifierAssignment:
            stmts.eval_modifier_assignment(node, env)
        case NodeType.Program:
            stmts.eval_program(node, env)
        case _:
            raise Exception(node)