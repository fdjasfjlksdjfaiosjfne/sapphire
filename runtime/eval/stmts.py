import parser.nodes as Nodes
from runtime.interpreter import evaluate
from runtime.env import Env
from runtime.eval.exprs import eval_code_block
import runtime.values as Values
from backend import errors
from runtime import native_fns

def eval_program(program: Nodes.ProgramNode, env: Env, /) -> None:
    eval_code_block(program.body, env)

def eval_assignment(assign: Nodes.AssignmentNode, env: Env, /) -> None:
    expr = evaluate(assign.idents_and_expr.pop(), env)
    for ident in assign.idents_and_expr:
        if not isinstance(ident, Nodes.IdentifierNode):
            raise Exception()
        env.assign(ident.symbol, expr)

def eval_var_declaration(decl: Nodes.VarDeclarationNode, env: Env, /) -> None:
    env.declare(decl.name, decl.value, decl.constant)

def eval_modifier_assignment(assign: Nodes.ModifierAssignmentNode, env: Env, /) -> None:
    import runtime.eval.inplaceops as iops
    if not isinstance(assign.assignee, Nodes.IdentifierNode):
        raise Exception()
    ident = assign.assignee
    rhs = evaluate(assign.value, env)
    match assign.assign_oper:
        case "+=":
            iops.eval_iadd(ident, rhs, env)
        case "-=":
            iops.eval_isub(ident, rhs, env)
        case "*=":
            iops.eval_imul(ident, rhs, env)
        case "/=":
            iops.eval_itruediv(ident, rhs, env)
        case "//=":
            iops.eval_ifloordiv(ident, rhs, env)
        case "**=":
            iops.eval_pow(ident, rhs, env)
        case "??=":
            iops.eval_coalescing(ident, rhs, env)
        case "@=":
            iops.eval_imatmul(ident, rhs, env)
        case "%=":
            iops.eval_imod(ident, rhs, env)
        case "..=":
            iops.eval_iconcat(ident, rhs, env)

def eval_break(node: Nodes.BreakNode, env: Env, /) -> None:
    # todo add label support
    raise errors.BreakLoop

def eval_conditional(node: Nodes.ConditionalNode, env: Env, /) -> None:
    cond = native_fns.bool(evaluate(node.condition, env))
    if not isinstance(cond, Values.NOT_IMPLEMENTED) and cond.value == True:
        eval_code_block(node.code_block, env)
    elif isinstance(cond, Values.NOT_IMPLEMENTED):
        raise Exception()
    else:
        if isinstance(node.otherwise, Nodes.CodeBlockNode):
            eval_code_block(node.otherwise, env)
        elif isinstance(node.otherwise, Nodes.ConditionalNode):
            eval_conditional(node.otherwise, env)

def eval_while_loop(loop: Nodes.WhileLoopNode, env: Env, /):
    while native_fns.bool(evaluate(loop.condition, env)):
        try:
            evaluate(loop.code_block, env)
        except errors.BreakLoop:
            # todo label support
            return
        except errors.ContinueLoop:
            # todo label support
            continue
    else:
        evaluate(loop.else_block, env)

def eval_glorified_while_loop(loop: Nodes.GlorifiedWhileLoopNode, env: Env, /):
    env = Env(parent = env)
    evaluate(loop.init, env)
    while native_fns.bool(evaluate(loop.condition, env)):
        try:
            evaluate(loop.code_block, env)
        except errors.BreakLoop:
            # todo label support
            return
        except errors.ContinueLoop:
            # todo label support
            continue
        finally:
            evaluate(loop.repeat, env)
    else:
        evaluate(loop.else_block, env)

def eval_scope_block(scope: Nodes.ScopeBlockNode, env: Env, /):
    env = Env(parent = env)
    evaluate(scope.code_block, env)