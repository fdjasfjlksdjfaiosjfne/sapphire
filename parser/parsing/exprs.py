from __future__ import annotations

import typing

from backend import errors
from parser.lexer import Token, TokenType
from parser.parser import eat
import parser.nodes as Nodes

# ^ The order of precendence, the top being the one that is processed first
# Note that the last will be called first
## [x] PARENTHESES ()
## [x] PrimaryExpr (int, float, string, etc.)
## [x] `Subscription[]`, `member.access`, `Call()`
## [x] Unary Operators (`!`, `not`, `~`, `-`, `+`, `*` | `++`, `--`)
## [x] `**`
## [x] `*` / `/` / `//` / `%`
## [x] `+` / `-`
## [] `|>`
## [x] `in` / `not in`
## [x] `<` / `>` / `>=` / `<=` / `==` / `!=`
## [x] `<=>`
## [x] `<<` / `>>`
## [x] `b&`
## [x] `b^`
## [x] `b|`
## [x] `&` / `and`
## [x] `|` / `or`
## [x] `^` / `xor`
## [x] Ternary Operator (`a ? b : c`)
## [] `[1, 2, 3, 4]` `{1, 2, 3, 4}` `{"a": "b"}` `{a: "b"}`
## [x] Assignment Operator (`:=`)

# $ Conveniece ¯\_(ツ)_/¯
def parse_expr(tokens: typing.List[Token]) -> Nodes.Expr:
    return parse_assignment_expr(tokens)

def parse_assignment_expr(tokens: typing.List[Token]) -> Nodes.Expr:
    lhs = parse_collections_expr(tokens)
    if tokens[0] == TokenType.WalrusOper:
        return Nodes.WalrusExpr(lhs, eat(tokens).value, parse_collections_expr(tokens))
    return lhs

def parse_collections_expr(tokens: typing.List[Token]):
    elements = []
    match tokens[0]:
        case TokenType.OpenCurlyBrace:
            eat(tokens)
            raise Exception()
        case TokenType.OpenSquareBracket:
            eat(tokens)
            ...
        case _:
            # $ There may or may not be a tuple here
            elements = [parse_ternary_expr(tokens)]
            while tokens[0] == TokenType.Comma:
                eat(tokens)
                elements.append()
            return elements[0]

def parse_ternary_expr(tokens: typing.List[Token]) -> Nodes.TernaryNode:
    cond = parse_logical_expr(tokens)
    if tokens[0] == TokenType.QuestionMark:
        eat(tokens)
        true_expr = parse_expr(tokens)
        if tokens[0] == TokenType.GDCologne:
            eat(tokens)
            return Nodes.TernaryNode(cond, true_expr, parse_expr(tokens))
        raise errors
    return cond

# @ Thinking of deprecating this operator...
def parse_coalescing_expr(tokens: typing.List[Token]) -> Nodes.BinaryNode:
    lhs = parse_logical_expr(tokens)
    if tokens[0] == TokenType.Coalescing:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_coalescing_expr(tokens))
    return lhs


def parse_logical_expr(tokens: typing.List[Token]) -> Nodes.BinaryNode:
    lhs = parse_binary_expr(tokens)
    if tokens[0] in {TokenType.Caret, TokenType.Xor}:
        eat(tokens)
        return Nodes.BinaryNode(lhs, TokenType.Xor, parse_logical_expr(tokens))
    if tokens[0] in {TokenType.VerticalBar, TokenType.Or}:
        eat(tokens)
        return Nodes.BinaryNode(lhs, TokenType.Or, parse_logical_expr(tokens))
    if tokens[0] in {TokenType.Andpersand, TokenType.And}:
        eat(tokens)
        return Nodes.BinaryNode(lhs, TokenType.And, parse_logical_expr(tokens))
    return lhs

def parse_binary_expr(tokens: typing.List[Token]) -> Nodes.BinaryNode:
    lhs = parse_spaceship_expr(tokens)
    if tokens[0] in {
        TokenType.BinaryXor, 
        TokenType.BinaryOr, 
        TokenType.BinaryAnd, 
        TokenType.LeftShift, 
        TokenType.RightShift
    }:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_binary_expr(tokens))
    return lhs

def parse_spaceship_expr(tokens: list[Token]) -> Nodes.BinaryNode:
    lhs = parse_contain_expr(tokens)
    if tokens[0] == TokenType.Spaceship:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_contain_expr(tokens))
    return lhs

def parse_contain_expr(tokens: list[Token]) -> Nodes.BinaryNode:
    lhs = parse_condition_expr(tokens)
    if tokens[0] in {TokenType.In, TokenType.NotIn}:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_condition_expr(tokens))

def parse_condition_expr(tokens: typing.List[Token]) -> Nodes.BinaryNode:
    comp_tokens = frozenset( [
        TokenType.GreaterThan, 
        TokenType.GreaterEqualThan, 
        TokenType.Equal, 
        TokenType.NotEqual, 
        TokenType.LessEqualThan, 
        TokenType.LessThan,
        ]
    )
    lhs = parse_additive_expr(tokens)
    if tokens[0] in comp_tokens:
        comp_tokens_list = []; exprs = []
        while tokens[0] in comp_tokens:
            comp_tokens_list.append(eat(tokens).type)
            exprs.append(parse_additive_expr(tokens))
        return Nodes.ComparisonNode(lhs, comp_tokens_list, exprs)
    return lhs

def parse_additive_expr(tokens: typing.List[Token]) -> Nodes.BinaryNode:
    lhs = parse_multiplicative_expr(tokens)
    if tokens[0] in {TokenType.Plus, TokenType.Minus}:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_additive_expr(tokens))
    return lhs

def parse_multiplicative_expr(tokens: typing.List[Token]) -> Nodes.BinaryNode:
    lhs = parse_exponentiative_expr(tokens)
    if tokens[0] in {TokenType.Asterisk, TokenType.TrueDivision, TokenType.FloorDivision, TokenType.Modulus}:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_multiplicative_expr(tokens))
    return lhs

def parse_exponentiative_expr(tokens: typing.List[Token]) -> Nodes.BinaryNode:
    lhs = parse_unary_expr(tokens)
    if tokens[0] == TokenType.Exponentiation:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_exponentiative_expr(tokens))
    return lhs

def parse_unary_expr(tokens: typing.List[Token]) -> Nodes.BinaryNode:
    """
    Parses unary expressions. This include:
    - Prefix: `++`, `--`, `!`, `~`, `not`, `*`, `+`, `-`
    - Postfix: `++`, `--`
    """
    ## Prefix
    if tokens[0] in {
            TokenType.Plus, TokenType.Minus, TokenType.Asterisk, 
            TokenType.Tilda, TokenType.Not, TokenType.Exclamation, 
            TokenType.Incre, TokenType.Decre
            }:
        attachment = eat(tokens).type
        expr = parse_primary_expr(tokens)
        return Nodes.UnaryNode(attachment, expr, "Prefix")
    
    # $ At this point there should be a expression at the start
    # $ Time to parse it.
    expr = parse_primary_expr(tokens)
    
    if tokens[0] in {TokenType.Incre, TokenType.Decre}:
        return Nodes.UnaryNode(expr, eat(tokens).type, "Postfix")
    return expr

def parse_member_subscription_call_expr(tokens: typing.List[Token]) -> Nodes.BinaryNode:
    # $ Parses both member access (a.b), subscription access (a[b]) and function call (a(b)) expressions.
    
    # ? Importing
    import mem_sub_call as msc                                                                                                                                                                                                                                                                                                            ;pass
    
    member = msc.parse_member_subscription_expr(tokens)
    
    if tokens[0] == TokenType.OpenParenthesis:
        return msc.parse_call_expr(tokens, member)
    return member

def parse_primary_expr(tokens: list[Token], exclude: set [
        typing.Literal [
            TokenType.Identifier,
            TokenType.Int,
            TokenType.Float,
            TokenType.Str,
            TokenType.Bool,
            TokenType.Null,
            TokenType.OpenParenthesis
        ]
    ] = {}) -> Nodes.Expr:
    match tokens[0]:
        case TokenType.Identifier if TokenType.Identifier not in exclude:
            return Nodes.IdentifierNode(eat(tokens).value)
        case TokenType.Int if TokenType.Int not in exclude:
            return Nodes.IntNode(int(eat(tokens).value))
        case TokenType.Float if TokenType.Float not in exclude:
            return Nodes.FloatNode(float(eat(tokens).value))
        case TokenType.Str if TokenType.Str not in exclude:
            val = eat(tokens).value
            # ? Collect the configuration
            return Nodes.StrNode(val)
        case TokenType.Bool if TokenType.Bool not in exclude:
            return Nodes.BoolNode(True if eat(tokens).value == "true" else False)
        case TokenType.Null if TokenType.Null not in exclude:
            eat(tokens)
            return Nodes.NullNode()
        case TokenType.OpenParenthesis if TokenType.OpenParenthesis not in exclude:
            eat(tokens)
            try:
                eat(tokens, TokenType.NewLine)
            finally: pass
            expr = parse_expr(tokens)
            try:
                eat(tokens, TokenType.NewLine)
            finally: pass
            eat(tokens, TokenType.CloseParenthesis)
            return expr
        case _:
            raise Exception(tokens)