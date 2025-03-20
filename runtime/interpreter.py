import runtime.values as V
from parser.nodes import NodeType, Stmt
from runtime.env import Environment

def evaluate(node: Stmt, env: Environment) -> V.RuntimeVal:
    import runtime.eval.exprs as exprs
    import runtime.eval.stmts as stmts
    match node.kind:
        case NodeType.Identifier:
            return exprs.eval_identifier(node, env)
        case NodeType.Int:
            return V.IntVal(node.value)
        case NodeType.Float:
            return V.FloatVal(node.value)
        case NodeType.Str:
            return V.StrVal(node.value)
        case NodeType.Bool:
            return V.BoolVal(node.value)
        case NodeType.Null:
            return V.NullVal()
        case NodeType.CodeBlock:
            code_block_env = Environment(env)
            return exprs.eval_code_block(node, code_block_env)
        case NodeType.BinaryExpr:
            return exprs.eval_binary_expr(node, env)
        case NodeType.Comparison:
            return exprs.eval_comparison_expr(node, env)
        case NodeType.Ternary:
            return exprs.eval_ternary_expr(node, env)
        # case NodeType.CallExpr:
        #     return exprs.eval_call_expr(node, env)
        case NodeType.Program:
            stmts.eval_program(node, env)
        case _:
            raise Exception(node)