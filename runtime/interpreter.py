import runtime.values as V
from parser.nodes import NT, Stmt
from runtime.env import Environment

def evaluate(node: Stmt, env: Environment) -> V.RuntimeVal:
    import runtime.eval.exprs as exprs
    import runtime.eval.stmts as stmts
    match node.kind:
        case NT.Identifier:
            return exprs.eval_identifier(node, env)
        case NT.Int:
            return V.IntVal(node.value)
        case NT.Float:
            return V.FloatVal(node.value)
        case NT.Str:
            return V.StrVal(node.value)
        case NT.Bool:
            return V.BoolVal(node.value)
        case NT.Null:
            return V.NullVal()
        case NT.Conditional:
            return exprs.eval_conditional(node, env)
        case NT.CodeBlock:
            code_block_env = Environment(env)
            return exprs.eval_code_block(node, code_block_env)
        case NT.BinaryExpr:
            return exprs.eval_binary_expr(node, env)
        case NT.Comparison:
            return exprs.eval_comparison_expr(node, env)
        case NT.Ternary:
            return exprs.eval_ternary_expr(node, env)
        # case NodeType.CallExpr:
        #     return exprs.eval_call_expr(node, env)
        case NT.Program:
            stmts.eval_program(node, env)
        case _:
            raise Exception(node)