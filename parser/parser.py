import typing
from parser.lexer import Token, TokenType, Tokenizer
import parser.nodes as Nodes
from backend import errors
from parser.parsing.stmts.stmts import Stmts
from parser.parsing.exprs.exprs import Exprs

class Parser(Stmts, Exprs):
    def __init__(self, source: str):
        self.source = source
        self.tokens: Tokenizer = Tokenizer(self.source)
    
    def parse_module(self) -> Nodes.ModuleNode:
        program = Nodes.ModuleNode()
        try:
            while self.tokens.peek() != TokenType.EoF:
                program.body.append(self.parse_stmt())
            return program
        except StopIteration:
            raise errors.InternalError(
                "The lexer has been exhausted prematurely but the "
                "parser doesn't seems to handle it properly"
            )

    @typing.override
    def peek(self, offset: int = 0) -> Token:
        return self.tokens.peek(offset)

    @typing.override
    def advance(
        self, 
        ts: typing.Sequence[TokenType] = [], 
        error: errors.SapphireError | None = None
    ) -> Token:
        return self.tokens.advance(ts, error = error)
    
    @typing.override
    def advance_matchings(self, ts: typing.Sequence[TokenType] = []):
        self.advance_matchings(ts)