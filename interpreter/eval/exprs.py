import typing
import itertools

from backend import errors
import parser.nodes as Nodes
from interpreter import values
from interpreter.env import Env
from lexer import (
    TokenType,
    BinaryOperators,
    UnaryOperators,
    InvertedComparisons
)
import runtime.eval.opers as opers
from interpreter.interpreter import evaluate
from backend.config import CONFIG


def eval_code_block(code_block: Nodes.CodeBlockNode, env: Env, /):
    if CONFIG.customization.function_hoisting:
        c = itertools.count(start = 1)
        code_block.body.sort(
            key = lambda v: 0 if isinstance(v, Nodes.FunctionDeclarationNode) else next(c)
        )
    for stmt in code_block:
        evaluate(stmt, env)
    return None

def eval_identifier(ident: Nodes.IdentifierNode, env: Env, /) -> values.RuntimeValue:
    return env.get(ident.symbol)

def eval_binary_expr(binop: Nodes.BinaryNode, env: Env, /) -> values.RuntimeValue:
    
    lhs, rhs = evaluate(binop.left, env), evaluate(binop.right, env)
    match binop.oper:
        case BinaryOperators.Addition:
            return opers.eval_add(lhs, rhs, env)

        case BinaryOperators.Subtraction:
            return opers.eval_sub(lhs, rhs, env)

        case BinaryOperators.Multiplication:
            return opers.eval_mul(lhs, rhs, env)
        
        case BinaryOperators.TrueDivision: 
            return opers.eval_truediv(lhs, rhs, env)
        
        case BinaryOperators.FloorDivision:
            return opers.eval_floordiv(lhs, rhs, env)
        
        case BinaryOperators.Modulus: 
            return opers.eval_mod(lhs, rhs, env)
        
        case BinaryOperators.Exponentiation: 
            return opers.eval_exp(lhs, rhs, env)

        case BinaryOperators.Spaceship: 
            return opers.eval_sps(lhs, rhs, env)

        case BinaryOperators.Concanentation: 
            return opers.eval_concat(lhs, rhs, env)
        
        case BinaryOperators.MatrixMultiplication: 
            return opers.eval_matmul(lhs, rhs, env)
        
        case BinaryOperators.BinaryAnd:
            return opers.eval_binaryand(lhs, rhs, env)
        
        case BinaryOperators.BinaryOr:
            return opers.eval_binaryor(lhs, rhs, env)
        
        case BinaryOperators.BinaryXor:
            return opers.eval_binaryxor(lhs, rhs, env)
        
        case BinaryOperators.LeftShift:
            return opers.eval_lshift(lhs, rhs, env)
        
        case BinaryOperators.RightShift:
            return opers.eval_rshift(lhs, rhs, env)
        
        case oper:
            raise errors.InternalError(
                f"BinaryExpr contains a binary operator that the system could not process ({oper!r})"
            )

def eval_comparison_expr(comp_expr: Nodes.ComparisonNode, env: Env, /) -> values.RuntimeValue:
    current = evaluate(comp_expr.left, env)
    for i, op in enumerate(comp_expr.operators):
        comparator = evaluate(comp_expr.exprs[i], env)
        match op:
            case BinaryOperators.LessThan | InvertedComparisons.LessThan:
                result = opers.eval_lt(current, comparator, env)
            case BinaryOperators.LessThanOrEqualTo | InvertedComparisons.LessThanOrEqualTo:
                result = opers.eval_le(current, comparator, env)
            case BinaryOperators.Equality | InvertedComparisons.Equality:
                result = opers.eval_eq(current, comparator, env)
            case BinaryOperators.Inequality:
                result = opers.eval_ne(current, comparator, env)
            case BinaryOperators.GreaterThanOrEqualTo | InvertedComparisons.GreaterThanOrEqualTo:
                result = opers.eval_ge(current, comparator, env)
            case BinaryOperators.GreaterThan | InvertedComparisons.GreaterThan:
                result = opers.eval_gt(current, comparator, env)
            case _:
                raise Exception()
        
        if not values.BoolValue(result).value:
            return values.FALSE
        else: pass
        
        current = comparator
    return values.TRUE

def eval_ternary_expr(expr: Nodes.TernaryNode, env: Env, /) -> values.RuntimeValue:
    cond = values.BoolValue(evaluate(expr.cond, env))
    if cond.value:
        return evaluate(expr.true, env)
    return evaluate(expr.false, env)

def eval_call_expr(expr: Nodes.CallNode, env: Env, /) -> values.RuntimeValue:
    call_rt = evaluate(expr.caller, env)
    if hasattr(call_rt, "call"):
        call_rt = typing.cast(values.FunctionValue, call_rt)
        return call_rt.call(env, expr.args.args, expr.args.kwargs)
    raise errors.TypeError(
        f"Object of type '{type(call_rt)}' is not callable"
    )

def eval_subscription(expr: Nodes.SubscriptionNode, env: Env, /) -> values.RuntimeValue:
    ...

def eval_walrus(assign: Nodes.WalrusNode, env: Env, /) -> values.RuntimeValue:
    if not isinstance(assign.assignee, Nodes.IdentifierNode):
        raise Exception()
    env.assign(assign.assignee.symbol, v := evaluate(assign.value, env))
    return v

def eval_unary(node: Nodes.UnaryNode, env: Env, /) -> values.RuntimeValue:
    raise errors.InProgress
    match node.attachment:
        case UnaryOperators.Increment:
            result = opers.eval_increment(evaluate(node.expr, env))
        case UnaryOperators.Decrement:
            result = opers.eval_decrement(evaluate(node.expr, env))
        case _:
            raise errors.InProgress