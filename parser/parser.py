import typing
from parser.lexer import Token, TokenType
import parser.nodes as Nodes

def produce_program_ast(tokens: typing.List[Token]) -> Nodes.ProgramNode:
    from parser.parsing.stmts import parse_stmt
    program = Nodes.ProgramNode()
    while tokens[0] != TokenType.EoF:
        program.body.append(parse_stmt(tokens))
        if tokens[0] != TokenType.EoF:
            eat(tokens, TokenType.NewLine, TokenType.Semicolon)
    return program

def eat(tokens: typing.List[Token], *types: typing.Union[TokenType, None], error: BaseException = None) -> Token:
    tkn = tokens.pop(0)
    if len(types) != 0:
        if tkn.type not in types:
            if error is None:
                raise ValueError(f"Error: {tkn} doesn't match type specified: {types}")
            raise error
    return tkn

