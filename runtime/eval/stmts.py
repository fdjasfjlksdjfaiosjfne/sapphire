import parser.nodes as Nodes
from runtime.interpreter import evaluate
from runtime.env import Env
from runtime.eval.exprs import eval_code_block
import runtime.values as Values
from backend import errors
from runtime import native_fns

def eval_program(program: Nodes.ModuleNode, env: Env, /) -> None:
    eval_code_block(program.body, env)

def eval_assignment(assign: Nodes.AssignmentNode, env: Env, /) -> None:
    expr = evaluate(assign.idents_and_expr.pop(), env)
    for ident in assign.idents_and_expr:
        if not isinstance(ident, Nodes.IdentifierNode):
            raise Exception()
        env.assign(ident.symbol, expr)

def eval_var_declaration(decl: Nodes.VarDeclarationNode, env: Env, /) -> None:
    raise errors.InternalError("Variable declaration is currently undergoing construction.")
    env.declare(decl.name, decl.value, decl.constant)

def eval_modifier_assignment(assign: Nodes.ModifierAssignmentNode, env: Env, /) -> None:
    import runtime.eval.inplaceops as iops
    if not isinstance(assign.assignee, Nodes.IdentifierNode):
        raise Exception()
    lhs = env.get(assign.assignee.symbol)
    rhs = evaluate(assign.value, env)
    right = assign.assign_oper[0] != "="
    match assign.assign_oper.removeprefix("=").removesuffix("="):
        case "+":
            iops.eval_iadd(lhs, rhs, right)
        case "-=":
            iops.eval_isub(lhs, rhs, right)
        case "*=":
            iops.eval_imul(lhs, rhs, right)
        case "/=":
            iops.eval_itruediv(lhs, rhs, right)
        case "//=":
            iops.eval_ifloordiv(lhs, rhs, right)
        case "**=":
            iops.eval_iexp(lhs, rhs, right)
        case "@=":
            iops.eval_imatmul(lhs, rhs, right)
        case "%=":
            iops.eval_imod(lhs, rhs, right)
        case "..=":
            iops.eval_iconcat(lhs, rhs, right)

def eval_break(node: Nodes.BreakNode, env: Env, /) -> None:
    # todo add label support
    raise errors.BreakLoop

def eval_conditional(node: Nodes.ConditionalNode, env: Env, /) -> None:
    cond = Values.Bool(evaluate(node.condition, env))
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
    while Values.Bool(evaluate(loop.condition, env)):
        try:
            evaluate(loop.code_block, env)
        except errors.BreakLoop:
            # todo label support
            return
        except errors.ContinueLoop:
            # todo label support
            continue
    else:
        if loop.else_block is not None:
            evaluate(loop.else_block, env)

def eval_glorified_while_loop(loop: Nodes.GlorifiedWhileLoopNode, env: Env, /):
    env = Env(parent = env)
    evaluate(loop.init, env)
    while Values.Bool(evaluate(loop.condition, env)):
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
        if loop.else_block is not None:
            evaluate(loop.else_block, env)

def eval_scope_block(scope: Nodes.ScopeBlockNode, env: Env, /):
    env = Env(parent = env)
    evaluate(scope.code_block, env)