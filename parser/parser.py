import typing
from parser.lexer.lexer import Token, TokenType, Tokenizer
from utils import config
import parser.nodes as Nodes
from backend import errors
from parser.parsing.stmts.stmts import Stmts
from parser.parsing.exprs.exprs import Exprs

class Parser(Stmts, Exprs):
    def __init__(self, source: str, conf: config.ConfigCls = config.ConfigCls()):
        self.source = source
        self.conf = conf
        self.tokens: Tokenizer = Tokenizer(self.source, conf)

    def parse_module(self) -> Nodes.ModuleNode:
        program = Nodes.ModuleNode()
        try:
            while self.tokens.peek() != TokenType.EoF:
                program.body.append(self._parse_stmt())
            return program
        except StopIteration:
            raise errors.InternalError(
                "The lexer has been exhausted prematurely but the "
                "parser doesn't seems to handle it properly"
            )