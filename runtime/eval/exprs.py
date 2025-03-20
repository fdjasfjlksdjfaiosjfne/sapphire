import parser.nodes as N
from parser.nodes import NodeType
import runtime.values as V
from runtime.env import Environment
from lexer.tokens import TokenType
import runtime.eval.binops as binops
import runtime.eval.conversions as converts
from typing import overload, Literal

@overload
def eval_code_block(code_block: N.CodeBlockNode, env: Environment) -> V.RuntimeVal: ...

@overload
def eval_code_block(code_block: N.CodeBlockNode, env: Environment, function: Literal[False] = False) -> V.RuntimeVal: ...

@overload
def eval_code_block(code_block: N.CodeBlockNode, env: Environment, function: Literal[True]) -> N.UnusableVal: ...

def eval_code_block(code_block: N.CodeBlockNode, env: Environment, function: bool = False) -> V.RuntimeVal:
    from runtime.interpreter import evaluate
    for stmt in code_block:
        if stmt == NodeType.Return:
            if function:
                return stmt.value
            raise Exception()
        print("stmt: " + repr(stmt))
        print("parsed: " + repr(evaluate(stmt, env)))
    return V.UnusableVal()

def eval_identifier(ident: N.IdentifierNode, env: Environment) -> V.RuntimeVal:
    if ident.symbol in env:
        return env[ident.symbol]
    raise Exception()

def eval_binary_expr(binop: N.BinaryExprNode, env: Environment) -> V.RuntimeVal:
    from runtime.interpreter import evaluate
    lhs, rhs = evaluate(binop.left, env), evaluate(binop.right, env)
    match binop.oper:
        case TokenType.Plus: return binops.eval_add(lhs, rhs, env)
        case TokenType.Minus: return binops.eval_sub(lhs, rhs, env)
        case TokenType.Asterisk: return binops.eval_mul(lhs, rhs, env)
        case TokenType.Divide: return binops.eval_div(lhs, rhs, env)
        case TokenType.Modulus: return binops.eval_mod(lhs, rhs, env)
        case TokenType.Exponentiation: return binops.eval_exp(lhs, rhs, env)
        case TokenType.Spaceship: return binops.eval_spaceship(lhs, rhs, env)
        case _: raise Exception()

def eval_comparison_expr(comp_expr: N.ComparisonNode, env: Environment) -> V.RuntimeVal:
    from runtime.interpreter import evaluate
    current = evaluate(comp_expr.left, env)
    for i, op in enumerate(comp_expr.operators):
        comparator = evaluate(comp_expr.exprs[i], env)
        match op:
            case TokenType.LessThan:
                result = binops.eval_lt(current, comparator, env)
            case TokenType.LessEqualThan:
                result = binops.eval_le(current, comparator, env)
            case TokenType.Equal:
                result = binops.eval_eq(current, comparator, env)
            case TokenType.NotEqual:
                result = binops.eval_ne(current, comparator, env)
            case TokenType.GreaterEqualThan:
                result = binops.eval_ge(current, comparator, env)
            case TokenType.GreaterThan:
                result = binops.eval_gt(current, comparator, env)
            case _:
                raise Exception()
        
        if not converts.bool(result).value:
            return V.BoolVal(False)
        else: pass
        
        current = comparator
    return V.BoolVal(True)

def eval_ternary_expr(expr: N.TernaryNode, env: Environment) -> V.RuntimeVal:
    from runtime.interpreter import evaluate
    cond = converts.bool(evaluate(expr.cond, env))
    if cond.value:
        return evaluate(expr.true, env)
    return evaluate(expr.false, env)

def eval_call_expr(expr, env: Environment) -> V.RuntimeVal:
    raise Exception()