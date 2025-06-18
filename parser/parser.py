import typing
from parser.lexer import Token, TokenType
import parser.nodes as Nodes

def produce_program_ast(tokens: typing.List[Token]) -> Nodes.Program:
    from parser.parsing.stmts import parse_stmts
    program = Nodes.Program()
    while at(tokens) != TokenType.EoF:
        program.body.append(parse_stmts(tokens))
        if at(tokens) != TokenType.EoF:
            eat(tokens, {TokenType.NewLine, TokenType.Semicolon})
    return program

def at(tokens: typing.List[Token]) -> TokenType:
    return tokens[0].type

def at_is(tokens: typing.List[Token], *types: TokenType) -> bool:
    return at(tokens) in types

def eat(tokens: typing.List[Token], *types: typing.Union[TokenType, typing.Set[TokenType], None]) -> Token:
    tkn = tokens.pop(0)
    if len(types) != 0:
        if tkn.type not in types:
            raise ValueError(f"Error: {tkn} doesn't match type specified: {types}")
    return tkn

