from __future__ import annotations

import typing
from backend import errors
from parser.lexer import Token, TokenType
from parser.parser import eat
import parser.nodes as Nodes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               # oh hello there
# ^ The order of precendence, the top being the one that is processed first
# Note that the last will be called first
## [x] PARENTHESES ()
## [x] PrimaryExpr (int, float, string, etc.)
## [x] 'Subscription[]', 'member.access', 'Call()'
## [x] Unary Operators ('!', 'not', '~', '-', '+', '*' | '++', '--')
## [x] '**'
## [x] '*' / '/' / '//' / '%'
## [x] '+' / '-'
## [] '|>'
## [x] 'in' / 'not in'
## [x] '<' / '>' / '>=' / '<=' / '==' / '!='
## [x] '<=>'
## [x] '<<' / '>>'
## [x] 'b&'
## [x] 'b^'
## [x] 'b|'
## [x] '&' / 'and'
## [x] '|' / 'or'
## [x] '^' / 'xor'
## [x] Ternary Operator ('a ? b : c')
## [x] '[1, 2, 3, 4]' '{1, 2, 3, 4}' '{"a": "b"}' '{a: "b"}'
## [x] Assignment Operator (':=')

def parse_expr(tokens: list[Token], /, **context) -> Nodes.ExprNode:
    expr = parse_assignment_expr(tokens, **context)

    # ^ Parsing tuples
    # & Don't ask why it's separated from the rest of collection expressions...
    # ^ ^ Explcit tuples
    if context.pop("allow_explicit_tuple", False) and tokens[0] == TokenType.Comma:
        # $ This is a tuple WITH parentheses
        # $ Remove 'in_parentheses'
        # $ The only place that gives 'allow_explicit_tuple' also gives 'in_parentheses' anyway
        context.pop("in_parentheses", None)
        
        if tokens[0] == TokenType.Comma:
            elements = [expr]
            while tokens[0] == TokenType.Comma:
                eat(tokens)
                if tokens[0] == TokenType.CloseParenthesis:
                    break
                elements.append(parse_expr(tokens, **context))
                # @ DO NOT EAT THE ')' TOKEN
            # ? As of now, the parse_primary_expr() function that call this one is still waiting for the expression
            # ? And then it will eat the ')' token
            # ! Eat it now will break everything
            # * Simply check for it instead, then throw an error if it's not there
            if tokens[0] != TokenType.CloseParenthesis:
                raise errors.SyntaxError("'(' is not closed")
            return Nodes.TupleNode(elements)
    
    # ^ ^ Implicit tuples
    if context.pop("allow_implicit_tuples", False):
        if tokens[0] == TokenType.Comma:
            elements = [expr]
            while tokens[0] == TokenType.Comma:
                eat(tokens)
                elements.append(parse_expr(tokens, **context))
            return Nodes.TupleNode(elements)
    
    return expr

def parse_assignment_expr(tokens: list[Token], /, **context) -> Nodes.ExprNode:
    lhs = parse_collections_expr(tokens, **context)
    if tokens[0] == TokenType.WalrusOper:
        return Nodes.WalrusExpr(lhs, eat(tokens).value, parse_collections_expr(tokens, **context))
    return lhs

def parse_collections_expr(tokens: list[Token], /, **context):
    match tokens[0]:
        case TokenType.OpenSquareBracket:
            expr = parse_expr(tokens, **context)
            if tokens[0] == TokenType.For:
                # $ This is a list comprehension
                return parse_comprehension(tokens, **context)
            # $ This is a list
            elements = [expr]
            while tokens[0] == TokenType.Comma:
                eat(tokens)
                if tokens[0] == TokenType.CloseSquareBracket:
                    break
                elements.append(parse_expr(tokens, **context))
            eat(tokens, TokenType.CloseSquareBracket, error = errors.SyntaxError("'[' is not closed"))
            return Nodes.ListNode(elements)
        case TokenType.OpenCurlyBrace:
            key_expr = parse_expr(tokens, **context)
            if tokens[0] == TokenType.GDCologne: # Don't ask
                eat(tokens)
                val_expr = parse_expr(tokens, **context)
                if tokens[0] == TokenType.For:
                    # $ This is a dictionary comprehension
                    return parse_dict_comprehension(tokens, pair = (key_expr, val_expr), **context)
                # $ This is a dictionary
                pairs = [(key_expr, val_expr)]
                while tokens[0] == TokenType.Comma:
                    eat(tokens)
                    if tokens[0] == TokenType.CloseCurlyBrace:
                        break
                    k = parse_expr(tokens, **context)
                    eat(tokens, TokenType.GDCologne)
                    v = parse_expr(tokens, **context)
                    pairs.append((k, v))
                eat(tokens, TokenType.CloseCurlyBrace, error = errors.SyntaxError("'{' is not closed"))
                return Nodes.DictNode(pairs)
            elif tokens[0] == TokenType.For:
                # $ This is a set comprehension
                return parse_comprehension(tokens, **context)
            else:
                # $ This is a set
                items = [key_expr]
                while tokens[0] == TokenType.Comma:
                    eat(tokens)
                    if tokens[0] == TokenType.CloseCurlyBrace:
                        break
                    items.append(parse_expr(tokens, **context))
                    eat(tokens, TokenType.CloseCurlyBrace, error = errors.SyntaxError("'{' is not closed"))
                    return Nodes.SetNode(items)
        case _:
            return parse_ternary_expr(tokens, **context)

def parse_comprehension(tokens: list[Token], /, **context):
    pass

def parse_dict_comprehension(tokens: list[Token], /, **context):
    pass

def parse_ternary_expr(tokens: list[Token], /, **context) -> Nodes.TernaryNode:
    cond = parse_logical_expr(tokens, **context)
    if tokens[0] == TokenType.QuestionMark:
        eat(tokens)
        true_expr = parse_expr(tokens, **context)
        if tokens[0] == TokenType.GDCologne:
            eat(tokens, **context)
            return Nodes.TernaryNode(cond, true_expr, parse_expr(tokens, **context))
        raise errors
    return cond

def parse_logical_expr(tokens: list[Token], /, **context) -> Nodes.BinaryNode:
    lhs = parse_binary_expr(tokens, **context)
    if tokens[0] in {TokenType.Caret, TokenType.Xor}:
        eat(tokens)
        return Nodes.BinaryNode(lhs, TokenType.Xor, parse_logical_expr(tokens, **context))
    if tokens[0] in {TokenType.VerticalBar, TokenType.Or}:
        eat(tokens)
        return Nodes.BinaryNode(lhs, TokenType.Or, parse_logical_expr(tokens, **context))
    if tokens[0] in {TokenType.Andpersand, TokenType.And}:
        eat(tokens)
        return Nodes.BinaryNode(lhs, TokenType.And, parse_logical_expr(tokens, **context))
    return lhs

def parse_binary_expr(tokens: list[Token], /, **context) -> Nodes.BinaryNode:
    lhs = parse_spaceship_expr(tokens, **context)
    if tokens[0] in {
        TokenType.BinaryXor, 
        TokenType.BinaryOr, 
        TokenType.BinaryAnd, 
        TokenType.LeftShift, 
        TokenType.RightShift
    }:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_binary_expr(tokens, **context))
    return lhs

def parse_spaceship_expr(tokens: list[Token], /, **context) -> Nodes.BinaryNode:
    lhs = parse_contain_expr(tokens, **context)
    if tokens[0] == TokenType.Spaceship:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_spaceship_expr(tokens, **context))
    return lhs

def parse_contain_expr(tokens: list[Token], /, **context) -> Nodes.BinaryNode:
    lhs = parse_condition_expr(tokens, **context)
    if tokens[0] in {TokenType.In, TokenType.NotIn}:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_contain_expr(tokens, **context))
    return lhs

def parse_condition_expr(tokens: list[Token], /, **context) -> Nodes.BinaryNode:
    comp_tokens = frozenset([
        TokenType.GreaterThan, 
        TokenType.GreaterEqualThan, 
        TokenType.Equal, 
        TokenType.NotEqual, 
        TokenType.LessEqualThan, 
        TokenType.LessThan,
    ])
    lhs = parse_additive_expr(tokens, **context)
    if tokens[0] in comp_tokens:
        comp_tokens_list = []; exprs = []
        while tokens[0] in comp_tokens:
            comp_tokens_list.append(eat(tokens).type)
            exprs.append(parse_additive_expr(tokens, **context))
        return Nodes.ComparisonNode(lhs, comp_tokens_list, exprs)
    return lhs

def parse_additive_expr(tokens: list[Token], /, **context) -> Nodes.BinaryNode:
    lhs = parse_multiplicative_expr(tokens, **context)
    if tokens[0] in {TokenType.Plus, TokenType.Minus}:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_additive_expr(tokens, **context))
    return lhs

def parse_multiplicative_expr(tokens: list[Token], /, **context) -> Nodes.BinaryNode:
    lhs = parse_exponentiative_expr(tokens, **context)
    if tokens[0] in {TokenType.Asterisk, TokenType.TrueDivision, TokenType.FloorDivision, TokenType.Modulus}:
        return Nodes.BinaryNode(lhs, eat(tokens).type, parse_multiplicative_expr(tokens, **context))
    return lhs

def parse_exponentiative_expr(tokens: list[Token], /, **context) -> Nodes.BinaryNode:
    lhs = parse_unary_expr(tokens, **context)
    if tokens[0] == TokenType.Exponentiation:
        return Nodes.BinaryNode(lhs, eat(tokens, **context).type, parse_exponentiative_expr(tokens, **context))
    return lhs

def parse_unary_expr(tokens: list[Token], /, **context) -> Nodes.BinaryNode:
    """
    Parses unary expressions. This include:
    - Prefix: '++', '--', '!', '~', 'not', '*', '+', '-'
    - Postfix: '++', '--'
    """
    ## Prefix
    if tokens[0] in {
            TokenType.Plus, TokenType.Minus, TokenType.Asterisk, 
            TokenType.Tilda, TokenType.Not, TokenType.Exclamation, 
            TokenType.Incre, TokenType.Decre
            }:
        attachment = eat(tokens).type
        expr = parse_primary_expr(tokens, **context)
        return Nodes.UnaryNode(attachment, expr, "Prefix")
    
    # $ At this point there should be a expression at the start
    # $ Time to parse it.
    expr = parse_primary_expr(tokens, **context)
    
    if tokens[0] in {TokenType.Incre, TokenType.Decre}:
        return Nodes.UnaryNode(expr, eat(tokens).type, "Postfix")
    return expr

def parse_member_subscription_call_expr(tokens: list[Token], /, **context) -> Nodes.BinaryNode:
    # $ Parses both member access (a.b), subscription access (a[b]) and function call (a(b)) expressions.
    
    # ? Importing
    import mem_sub_call as msc
    
    member = msc.parse_member_subscription_expr(tokens, **context)
    
    if tokens[0] == TokenType.OpenParenthesis:
        return msc.parse_call_expr(tokens, caller = member, **context)
    return member

def parse_primary_expr(tokens: list[Token], /, **context) -> Nodes.ExprNode:
    exclude = context.pop("exclude_create_node", [])
    match tokens[0]:
        case TokenType.Identifier if TokenType.Identifier not in exclude:
            return Nodes.IdentifierNode(eat(tokens).value)
        case TokenType.Int if TokenType.Identifier not in exclude:
            return Nodes.IntNode(int(eat(tokens).value))
        case TokenType.Float if TokenType.Float not in exclude:
            return Nodes.FloatNode(float(eat(tokens).value))
        case TokenType.Str if TokenType.Str not in exclude:
            val = eat(tokens).value
            ...
            return Nodes.StrNode(val)
        case TokenType.Bool if TokenType.Bool not in exclude:
            return Nodes.BoolNode(True if eat(tokens).value == "true" else False)
        case TokenType.Null if TokenType.Null not in exclude:
            eat(tokens)
            return Nodes.NullNode()
        case TokenType.OpenParenthesis if TokenType.OpenParenthesis not in exclude:
            eat(tokens)
            while tokens[0] == TokenType.NewLine:
                eat(tokens, TokenType.NewLine)
            expr = parse_expr(
                tokens, 
                in_parentheses = True, 
                allow_explicit_tuple = True,
                **context
            )
            while tokens[0] == TokenType.NewLine:
                eat(tokens, TokenType.NewLine)
            eat(tokens, TokenType.CloseParenthesis)
            return expr
        case _:
            raise errors.InternalError(f"Unable to parse tokens. Tokens: {tokens!r}")