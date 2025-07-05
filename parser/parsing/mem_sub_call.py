import typing

from parser.lexer import Token, TokenType
from parser.parser import eat
import parser.nodes as Nodes
from parser.parsing.exprs import parse_primary_expr, parse_expr

def parse_member_subscription_expr(tokens: list[Token], /, **context) -> Nodes.BinaryNode: 
    obj = parse_primary_expr(tokens, **context)
    while tokens[0] in {TokenType.Dot, TokenType.OpenSquareBracket}:
        propert: Nodes.ExprNode
        if eat(tokens) == TokenType.Dot:
            if tokens[0] == TokenType.Identifier:
                propert = eat(tokens, TokenType.Identifier)
            return Nodes.MemberAccessNode(obj, propert)
        else:
            propert = parse_expr(tokens, **context)
            eat(tokens, TokenType.CloseSquareBracket)
            return Nodes.SubscriptionNode(obj, propert)

def parse_call_expr(tokens: list[Token], /, **context) -> Nodes.CallNode:
    call_expr = Nodes.CallNode(context.pop("caller"), parse_call_args(tokens, **context))
    if tokens[0] == TokenType.OpenParenthesis:
        call_expr = parse_call_expr(tokens, caller = call_expr, **context)
    return call_expr

def parse_call_args(tokens: list[Token], /, **context) -> Nodes.CallArgumentList:
    eat(tokens, TokenType.OpenParenthesis)
    # ? Check if there's no arguments
    # ? If not, call cls.parse_positional_call_args()
    args = Nodes.CallArgumentList() if tokens[0] == TokenType.CloseParenthesis else parse_positional_call_args(tokens, **context)
    eat(tokens, TokenType.CloseParenthesis)
    return args

def parse_positional_call_args(tokens: list[Token], /, **context) -> Nodes.CallArgumentList:
    # $ At this point, there should be one or more arguments here.
    # $ So by that, just parse the first argument
    positional_args = []
    
    while tokens[0] == TokenType.Comma:
        eat(tokens)
        arg = parse_expr(tokens, **context)
        # > Check if the argument is actually a keyword argument
        # ? By looking at whether that 
        if isinstance(arg, Nodes.IdentifierNode) and tokens[0] == TokenType.AssignOper:
            return Nodes.CallArgumentList(positional_args, parse_keyword_call_args(tokens, arg.symbol, **context))
        positional_args.push(arg)
        
    return Nodes.CallArgumentList(positional_args)

def parse_keyword_call_args(tokens: list[Token], /, **context) -> typing.Dict[str, Nodes.ExprNode]:
    keyword_args: typing.Dict[str, Nodes.ExprNode] = {}
    eat(tokens, TokenType.AssignOper)
    keyword_args.setdefault(context.pop("initial_ident_name"), parse_expr(tokens, **context))
    if tokens[0] == TokenType.Comma:
        while tokens[0] == TokenType.Comma:
            # Exclude identifier
            key = eat(tokens, TokenType.Identifier).value
            eat(tokens, TokenType.AssignOper)
            keyword_args.setdefault(key.symbol, parse_expr(tokens, **context))
    elif not tokens[0] == TokenType.CloseParenthesis:
        raise Exception()
    return keyword_args