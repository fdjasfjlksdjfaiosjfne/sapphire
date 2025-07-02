import parser.nodes as Nodes
import runtime.values as Values
from runtime.env import Env
from parser.lexer import TokenType
import runtime.eval.binops as opers
import runtime.eval.conversions as convert
from runtime.interpreter import evaluate
import typing

def eval_code_block(code_block: Nodes.CodeBlock, env: Env) -> Values.RuntimeVal:
    for stmt in code_block:
        evaluate(stmt, env)
    return None

def eval_identifier(ident: Nodes.IdentifierNode, env: Env) -> Values.RuntimeVal:
    return env.get(ident.symbol)

def eval_binary_expr(binop: Nodes.BinaryNode, env: Env) -> Values.RuntimeVal:
    
    lhs, rhs = evaluate(binop.left, env), evaluate(binop.right, env)
    match binop.oper:
        case TokenType.Plus: 
            return opers.eval_add(lhs, rhs)
        
        case TokenType.Minus: 
            return opers.eval_sub(lhs, rhs)
        
        case TokenType.Asterisk: 
            return opers.eval_mul(lhs, rhs)
        
        case TokenType.TrueDivision: 
            return opers.eval_truediv(lhs, rhs)
        
        case TokenType.FloorDivision:
            return opers.eval_floordiv(lhs, rhs)
        
        case TokenType.Modulus: 
            return opers.eval_mod(lhs, rhs)
        
        case TokenType.Exponentiation: 
            return opers.eval_exp(lhs, rhs)
        
        case TokenType.Spaceship: 
            return opers.eval_sps(lhs, rhs)
        
        case TokenType.Concanentation: 
            return opers.eval_concat(lhs, rhs)
        
        case TokenType.At: 
            return opers.eval_matmul(lhs, rhs)
        
        case TokenType.BinaryAnd:
            return opers.eval_binaryand(lhs, rhs)
        
        case TokenType.BinaryOr:
            return opers.eval_binaryor(lhs, rhs)
        
        case TokenType.BinaryXor:
            return opers.eval_binaryxor(lhs, rhs)
        
        case TokenType.Elvis:
            return opers.eval_elvis(lhs, rhs)
        
        case TokenType.Coalescing:
            return opers.eval_coalescing(lhs, rhs)
        
        case TokenType.LeftShift:
            return opers.eval_left_shift(lhs, rhs)
        
        case TokenType.RightShift:
            return opers.eval_right_shift(lhs, rhs)
        
        case _: 
            raise Exception()

def eval_comparison_expr(comp_expr: Nodes.ComparisonNode, env: Env) -> Values.RuntimeVal:
    
    current = evaluate(comp_expr.left, env)
    for i, op in enumerate(comp_expr.operators):
        comparator = evaluate(comp_expr.exprs[i], env)
        match op:
            case TokenType.LessThan:
                result = opers.eval_lt(current, comparator)
            case TokenType.LessEqualThan:
                result = opers.eval_le(current, comparator)
            case TokenType.Equal:
                result = opers.eval_eq(current, comparator)
            case TokenType.NotEqual:
                result = opers.eval_ne(current, comparator)
            case TokenType.GreaterEqualThan:
                result = opers.eval_ge(current, comparator)
            case TokenType.GreaterThan:
                result = opers.eval_gt(current, comparator)
            case _:
                raise Exception()
        
        if not convert.bool(result).value:
            return Values.Bool(False)
        else: pass
        
        current = comparator
    return Values.Bool(True)

def eval_ternary_expr(expr: Nodes.TernaryNode, env: Env) -> Values.RuntimeVal:
    cond = convert.bool(evaluate(expr.cond, env))
    if cond.value:
        return evaluate(expr.true, env)
    return evaluate(expr.false, env)

def eval_call_expr(expr: Nodes.CallNode, env: Env) -> Values.RuntimeVal:
    raise Exception()

def eval_walrus(assign: Nodes.WalrusNode, env: Env) -> Values.RuntimeVal:
    if not isinstance(assign.assignee, Nodes.IdentifierNode):
        raise Exception()
    env.assign(assign.assignee.symbol, assign.value)
    return assign.value 

def eval_increment(ident: Nodes.IdentifierNode, pos: typing.Literal['Prefix', 'Postfix'], env: Env) -> Values.RuntimeVal:
    name = ident.symbol
    env = env.resolve(name)
    val = env.get(name)
    
    # x++ ++x
    if isinstance(val, Values.Number):
        env.assign(ident.symbol, val.value + 1)
        return env.get(ident.symbol) if pos == "Prefix" else val

def eval_decrement(ident: Nodes.IdentifierNode, pos: typing.Literal['Prefix', 'Postfix'], env: Env) -> Values.RuntimeVal:
    name = ident.symbol
    env = env.resolve(name)
    val = env.get(name)
    
    # x-- --x
    if isinstance(val, Values.Number):
        env.assign(ident.symbol, val.value - 1)
        return env.get(ident.symbol) if pos == "Prefix" else val

def eval_unary(node: Nodes.UnaryNode, env: Env) -> Values.RuntimeVal:
    pos = node.position
    if node.attachment in {TokenType.Incre, TokenType.Decre}:
        if not isinstance(node.expr, Nodes.IdentifierNode):
            raise Exception()
        return (eval_increment if node.attachment == TokenType.Incre else eval_decrement)(node.attachment, pos, env)