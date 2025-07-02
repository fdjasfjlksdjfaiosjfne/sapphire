import typing

from parser.lexer import Token, TokenType
from parser.parser import at, eat, at_is
import parser.nodes as Nodes
from parser.parsing.exprs import parse_primary_expr, parse_expr

def parse_member_subscription_expr(tokens: typing.List[Token]) -> Nodes.BinaryNode: 
    obj = parse_primary_expr(tokens)
    while at_is(tokens, TokenType.Dot, TokenType.OpenSquareBracket):
        propert: Nodes.Expr
        if eat(tokens) == TokenType.Dot:
            if at_is(tokens, TokenType.Identifier):
                propert = eat(tokens, TokenType.Identifier)
            return Nodes.MemberAccessNode(obj, propert)
        else:
            propert = parse_expr(tokens)
            eat(tokens, TokenType.CloseSquareBracket)
            return Nodes.SubscriptionNode(obj, propert)

def parse_call_expr(tokens: typing.List[Token], caller: Nodes.Expr) -> Nodes.CallNode:
    call_expr = Nodes.CallNode(caller, parse_call_args(tokens))
    if (at_is(tokens, TokenType.OpenParenthesis)):
        call_expr = parse_call_expr(tokens, call_expr)
    return call_expr

def parse_call_args(tokens: typing.List[Token]) -> Nodes.CallArgumentList:
    eat(tokens, TokenType.OpenParenthesis)
    # ? Check if there's no arguments
    # ? If not, call cls.parse_positional_call_args()
    args = Nodes.CallArgumentList() if at_is(tokens, TokenType.CloseParenthesis) else parse_positional_call_args(tokens)
    eat(tokens, TokenType.CloseParenthesis)
    return args

def parse_positional_call_args(tokens: typing.List[Token]) -> Nodes.CallArgumentList:
    # $ At this point, there should be one or more arguments here.
    # $ So by that, just parse the first argument
    positional_args = []
    
    while at_is(tokens, TokenType.Comma):
        eat(tokens)
        arg = parse_expr(tokens)
        # > Check if the argument is actually a keyword argument
        # ? By looking at whether that 
        if isinstance(arg, Nodes.IdentifierNode) and at_is(tokens, TokenType.AssignOper):
            return Nodes.CallArgumentList(positional_args, parse_keyword_call_args(tokens, arg.symbol))
        positional_args.push(arg)
        
    return Nodes.CallArgumentList(positional_args)

def parse_keyword_call_args(tokens: typing.List[Token], initial_ident_name: str) -> typing.Dict[str, Nodes.Expr]:
    keyword_args: typing.Dict[str, Nodes.Expr] = {}
    eat(tokens, TokenType.AssignOper)
    keyword_args.setdefault(initial_ident_name, parse_expr(tokens))
    if at_is(tokens, TokenType.Comma):
        while at_is(tokens, TokenType.Comma):
            # Exclude identifier
            key = parse_primary_expr(
                tokens,
                {
                TokenType.Int, 
                TokenType.Float, 
                TokenType.Str, 
                TokenType.Bool, 
                TokenType.Null, 
                TokenType.OpenParenthesis
                }
            )
            eat(tokens, TokenType.AssignOper)
            keyword_args.setdefault(key.symbol, parse_expr(tokens))
    elif not at_is(tokens, TokenType.CloseParenthesis):
        raise Exception()
    return keyword_args