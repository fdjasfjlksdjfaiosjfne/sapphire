import typing
from parser.lexer import Token, TokenType
import parser.nodes as Nodes

def produce_program_ast(tokens: typing.List[Token]) -> Nodes.ProgramNode:
    from parser.parsing.stmts import parse_stmts
    program = Nodes.ProgramNode()
    while tokens[0] != TokenType.EoF:
        program.body.append(parse_stmts(tokens))
        if tokens[0] != TokenType.EoF:
            eat(tokens, TokenType.NewLine, TokenType.Semicolon)
    return program

def eat(tokens: typing.List[Token], *types: typing.Union[TokenType, None]) -> Token:
    tkn = tokens.pop(0)
    if len(types) != 0:
        if tkn.type not in types:
            raise ValueError(f"Error: {tkn} doesn't match type specified: {types}")
    return tkn

