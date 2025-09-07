import typing
from lexer import TokenType, Tokenizer
from backend import config
import parser.nodes as Nodes
from backend import errors
from parser.stmts.stmts import Stmts
from parser.exprs.exprs import Exprs

class Parser(Stmts, Exprs):
    def __init__(self, source: str, conf: config.RootConfigCls = config.RootConfigCls()):
        self.source = source
        self.conf = conf
        self.tokens: Tokenizer = Tokenizer(self.source, conf)

    def parse_module(self) -> Nodes.ModuleNode:
        program = Nodes.ModuleNode()
        try:
            self._advance_matchings(self._STATEMENT_SEPARATORS)
            while self._peek().type != TokenType.EoF:
                program.body.append(self._parse_stmt())
                if not self._advance_matchings(self._STATEMENT_SEPARATORS):
                    raise errors.SyntaxError("Expecting a statement separator (; or new line)")
            return program
        except StopIteration:
            raise errors.InternalError(
                "The lexer has been exhausted prematurely but the "
                "parser doesn't seems to handle it properly"
            )
        except errors.BaseSapphireError as e:
            # Debugging purposes
            e.add_note(f"Remaining:\n{self.tokens.remaining()}")
            e.add_note(f"Current token: {self._peek().type}")
            e.add_note(f"Current token stream:\n{self.tokens.tokens}")
            e.add_note(f"Current program:\n{program.body.body}")
            raise e