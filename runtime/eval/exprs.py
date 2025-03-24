from parser.nodes import (
    NodeType,
    CodeBlock,
    Identifier, 
    Binary,
    Comparison,
    Ternary,
    Conditional,
    Call,
    Unary,
    WalrusExpr
)
from runtime.values import RuntimeVal, ValueType, Bool
from runtime.env import Env
from lexer.tokens import TokenType
import runtime.eval.binops as opers
import runtime.eval.conversions as convert
from runtime.interpreter import evaluate
from typing import Literal

def eval_code_block(code_block: CodeBlock, env: Env) -> RuntimeVal:
    for stmt in code_block:
        e = evaluate(stmt, env)
        print("stmt: " + repr(stmt))
        print("parsed: " + repr(e))
    return None

def eval_identifier(ident: Identifier, env: Env) -> RuntimeVal:
    return env.get(ident.symbol)

def eval_binary_expr(binop: Binary, env: Env) -> RuntimeVal:
    
    lhs, rhs = evaluate(binop.left, env), evaluate(binop.right, env)
    match binop.oper:
        case TokenType.Plus: 
            return opers.eval_add(lhs, rhs, env)
        
        case TokenType.Minus: 
            return opers.eval_sub(lhs, rhs, env)
        
        case TokenType.Asterisk: 
            return opers.eval_mul(lhs, rhs, env)
        
        case TokenType.TrueDivision: 
            return opers.eval_true_div(lhs, rhs, env)
        
        case TokenType.FloorDivision:
            return opers.eval_floor_div(lhs, rhs, env)
        
        case TokenType.Modulus: 
            return opers.eval_mod(lhs, rhs, env)
        
        case TokenType.Exponentiation: 
            return opers.eval_pow(lhs, rhs, env)
        
        case TokenType.Spaceship: 
            return opers.eval_spaceship(lhs, rhs, env)
        
        case TokenType.Concanentation: 
            return opers.eval_concat(lhs, rhs, env)
        
        case TokenType.At: 
            return opers.eval_matmul(lhs, rhs, env)
        
        case _: 
            raise Exception()

def eval_comparison_expr(comp_expr: Comparison, env: Env) -> RuntimeVal:
    
    current = evaluate(comp_expr.left, env)
    for i, op in enumerate(comp_expr.operators):
        comparator = evaluate(comp_expr.exprs[i], env)
        match op:
            case TokenType.LessThan:
                result = opers.eval_lt(current, comparator, env)
            case TokenType.LessEqualThan:
                result = opers.eval_le(current, comparator, env)
            case TokenType.Equal:
                result = opers.eval_eq(current, comparator, env)
            case TokenType.NotEqual:
                result = opers.eval_ne(current, comparator, env)
            case TokenType.GreaterEqualThan:
                result = opers.eval_ge(current, comparator, env)
            case TokenType.GreaterThan:
                result = opers.eval_gt(current, comparator, env)
            case _:
                raise Exception()
        
        if not convert.bool(result).value:
            return Bool(False)
        else: pass
        
        current = comparator
    return Bool(True)

def eval_ternary_expr(expr: Ternary, env: Env) -> RuntimeVal:
    cond = convert.bool(evaluate(expr.cond, env))
    if cond.value:
        return evaluate(expr.true, env)
    return evaluate(expr.false, env)

def eval_call_expr(expr: Call, env: Env) -> RuntimeVal:
    raise Exception()

def eval_conditional(node: Conditional, env: Env) -> RuntimeVal:
    cond = convert.bool(evaluate(node.condition, env))
    if cond != ValueType.NotImplemented and cond == True:
        print("TRUE")
        eval_code_block(node.code_block, env)
    elif cond == ValueType.NotImplemented:
        raise Exception()
    else:
        print("FALSE")
        if node.otherwise == NodeType.CodeBlock:
            eval_code_block(node.otherwise, env)
        eval_conditional(node.otherwise)

def eval_walrus(assign: WalrusExpr, env: Env) -> RuntimeVal:
    if assign.assignee != TokenType.Identifier: # TODO Support more types idrk lmao
        raise Exception()
    env.assign(assign.assignee.symbol, assign.value)
    return assign.value 

def eval_increment(ident: Identifier, pos: Literal['Prefix', 'Postfix'], env: Env) -> RuntimeVal:
    name = ident.symbol
    env = env.resolve(name)
    val = env.get(name)
    
    # x++ ++x
    if val == ValueType.Number:
        env.assign(ident.symbol, val.value + 1)
        return env.get(ident.symbol) if pos == "Prefix" else val

def eval_decrement(ident: Identifier, pos: Literal['Prefix', 'Postfix'], env: Env) -> RuntimeVal:
    name = ident.symbol
    env = env.resolve(name)
    val = env.get(name)
    
    # x-- --x
    if val == ValueType.Number:
        env.assign(ident.symbol, val.value - 1)
        return env.get(ident.symbol) if pos == "Prefix" else val

def eval_unary(node: Unary, env: Env) -> RuntimeVal:
    pos = node.position
    if node.attachment in {TokenType.Incre, TokenType.Decre}:
        if node.expr != NodeType.Identifier: # TODO Support more types idrk lmao
            raise Exception()
        return (eval_increment if node.attachment == TokenType.Incre else eval_decrement)(node.attachment, pos, env)
    