import typing

from parser.lexer import Token, TokenType
from parser.parser import at, eat, at_is
import parser.nodes as Nodes

# $ 

# ^ The order of precendence, the top being the one that is processed first
# Note that the last will be called first
## [x] PARENTHESES ()
## [x] PrimaryExpr (int, float, string, etc.)
## [] Type Hint (?)
## [x] `Call()`
## [x] `Subscription[]`, `member.access`
## [x] Unary Operators (`!`, `not`, `~`, `-`, `+`, `*` | `++`, `--`)
## [x] `**`
## [x] `*` / `/` / `//` / `%`
## [x] `+` / `-`
## [] `|>`
## [x] `<` / `>` / `>=` / `<=` / `==` / `!=`
## [] `<=>`
## [x] `<<` / `>>`
## [x] `b&`
## [x] `b^`
## [x] `b|`
## [x] `&` / `and`
## [x] `|` / `or`
## [x] `^` / `xor`
## [] `??` Coalescing
## [] `?:` Elvis
## [x] Ternary Operator (`a ? b [: c]`)
## [] `[1, 2, 3, 4]` `{1, 2, 3, 4}` `{"a": "b"}` `{a: "b"}`
## [x] Assignment Operator (`:=`)

# $ Conveniece ¯\_(ツ)_/¯
def parse_expr(tokens: typing.List[Token]) -> Nodes.Expr:
    return parse_assignment_expr(tokens)

def parse_assignment_expr(tokens: typing.List[Token]) -> Nodes.AllExprTypeHint:
    lhs = parse_collections_expr(tokens)
    if at_is(tokens, TokenType.WalrusOper):
        return Nodes.WalrusExpr(lhs, eat(tokens).value, parse_collections_expr(tokens))
    return lhs

def parse_collections_expr(tokens: typing.List[Token]):
    match at(tokens):
        case TokenType.OpenCurlyBrace:
            eat(tokens)
            raise Exception()
        case TokenType.OpenSquareBracket:
            eat(tokens)
            raise Exception()
        case _:
            return parse_ternary_expr(tokens)

def parse_ternary_expr(tokens: typing.List[Token]) -> Nodes.Ternary:
    cond = parse_logical_expr(tokens)
    if at_is(tokens, TokenType.QuestionMark):
        eat(tokens)
        true_expr = parse_expr(tokens)
        if at_is(tokens, TokenType.GDCologne):
            eat(tokens)
            return Nodes.Ternary(cond, true_expr, parse_expr(tokens))
        raise Exception("no else")
    return cond

def parse_elvis_expr(tokens: typing.List[Token]) -> Nodes.Binary:
    lhs = parse_coalescing_expr(tokens)
    if at_is(tokens, TokenType.Elvis):
        return Nodes.Binary(lhs, TokenType.Elvis, parse_elvis_expr(tokens))
    return lhs

def parse_coalescing_expr(tokens: typing.List[Token]) -> Nodes.Binary:
    lhs = parse_logical_expr(tokens)
    if at_is(tokens, TokenType.Coalescing):
        return Nodes.Binary(lhs, TokenType.Coalescing, parse_coalescing_expr(tokens))
    return lhs

def parse_logical_expr(tokens: typing.List[Token]) -> Nodes.Binary:
    lhs = parse_binary_expr(tokens)
    if at_is(tokens, TokenType.Caret, TokenType.Xor):
        return Nodes.Binary(lhs, TokenType.Xor, parse_logical_expr(tokens))
    if at_is(tokens, TokenType.VerticalBar, TokenType.Or):
        return Nodes.Binary(lhs, TokenType.Or, parse_logical_expr(tokens))
    if at_is(tokens, TokenType.Andpersand, TokenType.And):
        return Nodes.Binary(lhs, TokenType.And, parse_logical_expr(tokens))
    return lhs

def parse_binary_expr(tokens: typing.List[Token]) -> Nodes.Binary:
    lhs = parse_spaceship_expr(tokens)
    if at_is(tokens, TokenType.BinaryXor):
        return Nodes.Binary(lhs, TokenType.BinaryXor, parse_binary_expr(tokens))
    if at_is(tokens, TokenType.BinaryOr):
        return Nodes.Binary(lhs, TokenType.BinaryOr, parse_binary_expr(tokens))
    if at_is(tokens, TokenType.BinaryAnd):
        return Nodes.Binary(lhs, TokenType.BinaryOr, parse_binary_expr(tokens))
    if at_is(tokens, TokenType.LeftShift):
        return Nodes.Binary(lhs, TokenType.LeftShift, parse_binary_expr(tokens))
    if at_is(tokens, TokenType.RightShift):
        return Nodes.Binary(lhs, TokenType.RightShift, parse_binary_expr(tokens))
    return lhs

def parse_spaceship_expr(tokens: typing.List[Token]) -> Nodes.Binary:
    lhs = parse_condition_expr(tokens)
    if at_is(tokens, TokenType.Spaceship):
        return Nodes.Binary(lhs, TokenType.Spaceship, parse_spaceship_expr(tokens))
    return lhs

def parse_condition_expr(tokens: typing.List[Token]) -> Nodes.Binary:
    comp_tokens = frozenset( [
        TokenType.GreaterThan, 
        TokenType.GreaterEqualThan, 
        TokenType.Equal, 
        TokenType.NotEqual, 
        TokenType.LessEqualThan, 
        TokenType.LessThan,
        TokenType.Spaceship
        ]
    )
    lhs = parse_additive_expr(tokens)
    if at_is(tokens, *comp_tokens):
        comp_tokens = []; exprs = []
        while at_is(tokens, *comp_tokens):
            comp_tokens.append(eat(tokens).type)
            exprs.append(parse_additive_expr(tokens))
        return Nodes.Comparison(lhs, comp_tokens, exprs)
    return lhs

def parse_additive_expr(tokens: typing.List[Token]) -> Nodes.Binary:
    lhs = parse_multiplicative_expr(tokens)
    if at_is(tokens, TokenType.Plus, TokenType.Minus):
        return Nodes.Binary(lhs, eat(tokens).type, parse_additive_expr(tokens))
    return lhs

def parse_multiplicative_expr(tokens: typing.List[Token]) -> Nodes.Binary:
    lhs = parse_exponentiative_expr(tokens)
    if at_is(tokens, 
             TokenType.Asterisk, TokenType.TrueDivision, 
             TokenType.FloorDivision, TokenType.Modulus):
        return Nodes.Binary(lhs, eat(tokens).type, parse_multiplicative_expr(tokens))
    return lhs

def parse_exponentiative_expr(tokens: typing.List[Token]) -> Nodes.Binary:
    lhs = parse_unary_expr(tokens)
    if at_is(tokens, TokenType.Exponentiation):
        return Nodes.Binary(lhs, eat(tokens).type, parse_exponentiative_expr(tokens))
    return lhs

def parse_unary_expr(tokens: typing.List[Token]) -> Nodes.Binary:
    """
    Parses unary expressions. This include:
    - Prefix: `++`, `--`, `!`, `~`, `not`, `*`, `+`, `-`
    - Postfix: `++`, `--`
    """
    ## Prefix
    if at_is(
            tokens, 
            TokenType.Plus, TokenType.Minus, TokenType.Asterisk, 
            TokenType.Tilda, TokenType.Not, TokenType.Exclamation, 
            TokenType.Incre, TokenType.Decre
            ):
        attachment = eat(tokens).type
        expr = parse_primary_expr(tokens)
        return Nodes.Unary(attachment, expr, "Prefix")
    
    # $ At this point there should be a expression at the start
    # $ Time to parse it.
    expr = parse_primary_expr(tokens)
    
    if at_is(tokens, TokenType.Incre, TokenType.Decre):
        return Nodes.Unary(expr, eat(tokens).type, "Postfix")
    return expr

def parse_member_subscription_call_expr(tokens: typing.List[Token]) -> Nodes.Binary:
    # $ Parses both member access (a.b), subscription access (a[b]) and function call (a(b)) expressions.
    
    # ? Importing
    import mem_sub_call as msc
    
    member = msc.parse_member_subscription_expr(tokens)
    
    if at_is(tokens, TokenType.OpenParenthesis):
        return msc.parse_call_expr(tokens, member)
    return member

def parse_primary_expr(tokens: typing.List[Token], exclude: typing.Set [
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
    match at(tokens):
        case TokenType.Identifier if TokenType.Identifier not in exclude:
            return Nodes.Identifier(eat(tokens).value)
        case TokenType.Int if TokenType.Int not in exclude:
            return Nodes.Int(int(eat(tokens).value))
        case TokenType.Float if TokenType.Float not in exclude:
            return Nodes.Float(float(eat(tokens).value))
        case TokenType.Str if TokenType.Str not in exclude:
            return Nodes.Str(eat(tokens).value)
        case TokenType.Bool if TokenType.Bool not in exclude:
            return Nodes.Bool(True if eat(tokens).value == "true" else False)
        case TokenType.Null if TokenType.Null not in exclude:
            eat(tokens)
            return Nodes.Null()
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