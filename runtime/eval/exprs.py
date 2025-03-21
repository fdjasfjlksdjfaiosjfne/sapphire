import parser.nodes as N
from parser.nodes import NT
import runtime.values as V
from runtime.values import RuntimeVal, ValueType as VT
from runtime.env import Environment
from lexer.tokens import TokenType
import runtime.eval.binops as binops
import runtime.eval.conversions as convert
from runtime.interpreter import evaluate
from typing import Union

def eval_code_block(code_block: N.CodeBlockNode, env: Environment) -> RuntimeVal:
    for stmt in code_block:
        e = evaluate(stmt, env)
        print("stmt: " + repr(stmt))
        print("parsed: " + repr(e))
    return None

def eval_identifier(ident: N.IdentifierNode, env: Environment) -> RuntimeVal:
    if ident.symbol in env:
        return env[ident.symbol]
    

def eval_binary_expr(binop: N.BinaryExprNode, env: Environment) -> RuntimeVal:
    
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

def eval_comparison_expr(comp_expr: N.ComparisonNode, env: Environment) -> RuntimeVal:
    
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
        
        if not convert.bool(result).value:
            return V.BoolVal(False)
        else: pass
        
        current = comparator
    return V.BoolVal(True)

def eval_ternary_expr(expr: N.TernaryNode, env: Environment) -> RuntimeVal:
    cond = convert.bool(evaluate(expr.cond, env))
    if cond.value:
        return evaluate(expr.true, env)
    return evaluate(expr.false, env)

def eval_call_expr(expr, env: Environment) -> RuntimeVal:
    raise Exception()

def eval_conditional(node: N.ConditionalNode, env: Environment) -> RuntimeVal:
    cond = convert.bool(evaluate(node.condition, env))
    if cond != VT.NotImplemented and cond == True:
        print("TRUE")
        eval_code_block(node.code_block, env)
    elif cond == VT.NotImplemented:
        raise Exception()
    else:
        print("FALSE")
        if node.otherwise == NT.CodeBlock:
            eval_code_block(node.otherwise, env)
        eval_conditional(node.otherwise)