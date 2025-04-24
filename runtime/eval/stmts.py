import parser.nodes as Nodes
from runtime.interpreter import evaluate
from runtime.env import Env

def eval_program(program: Nodes.Program, env: Env) -> None:
    from runtime.eval.exprs import eval_code_block
    eval_code_block(program.body, env)
    return None

def eval_assignment(assign: Nodes.Assignment, env: Env) -> None:
    expr = evaluate(assign.idents_and_expr.pop(), env)
    for ident in assign.idents_and_expr:
        if not isinstance(ident, Nodes.Identifier):
            raise Exception()
        env.assign(ident.symbol, expr)

def eval_var_declaration(decl: Nodes.VarDeclaration, env: Env) -> None:
    env.declare(decl.name, decl.value, decl.constant)

def eval_modifier_assignment(assign: Nodes.ModifierAssignment, env: Env) -> None:
    import runtime.eval.modifierops as mops
    if not isinstance(assign.assignee, Nodes.Identifier):
        raise Exception()
    ident = assign.assignee
    rhs = evaluate(assign.value, env)
    match assign.assign_oper:
        case "+=":
            mops.eval_add(ident, rhs, env)
        case "-=":
            mops.eval_sub(ident, rhs, env)
        case "*=":
            mops.eval_mul(ident, rhs, env)
        case "/=":
            mops.eval_true_div(ident, rhs, env)
        case "//=":
            mops.eval_floor_div(ident, rhs, env)
        case "**=":
            mops.eval_pow(ident, rhs, env)
        case "??=":
            mops.eval_coalescing(ident, rhs, env)
        case "@=":
            mops.eval_matmul(ident, rhs, env)
        case "%=":
            mops.eval_mod(ident, rhs, env)
        case "..=":
            mops.eval_concat(ident, rhs, env)