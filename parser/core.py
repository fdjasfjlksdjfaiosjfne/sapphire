from abc import ABC, abstractmethod
import typing

from backend import errors
from lexer import Token, TokenType, Tokenizer, TokenTypeSequence, TokenTypeEnum
from backend.config import RootConfigCls, CONFIG
from parser import nodes

class ParserNamespaceSkeleton(ABC):
    tokens: Tokenizer
    conf: RootConfigCls
    if CONFIG.customization.uncategorized.semicolon_required:
        _STATEMENT_SEPARATORS = [TokenType.Symbols.StatementSeparator]
    else:
        _STATEMENT_SEPARATORS = [TokenType.Symbols.StatementSeparator, TokenType.NewLine]

    @typing.final
    def __getattribute__(self, attr: str):
        if super().__getattribute__("__class__").__name__ != "Parser":
            raise errors.InternalError(
                "An attempt to access an attribute from an incomplete parser namespace at " \
                "runtime has been detected. Please use the full 'Parser()' class instead of just " \
                "poking at an imcomplete stub."
            )
        return super().__getattribute__(attr)

    def _peek(self, offset: int = 0) -> Token:
        return self.tokens.peek(offset)

    def _advance(
        self, 
        ts: TokenTypeSequence = [], 
        error: errors.BaseSapphireError | None = None
    ) -> Token:
        return self.tokens.advance(ts, error = error)
    
    def _advance_matchings(self, ts: typing.Sequence[TokenType] = []):
        self._advance_matchings(ts)
    
    @staticmethod
    def _to_token_sequence(t: TokenTypeSequence, **context) -> tuple[TokenTypeEnum, ...]:
        return (t, ) if isinstance(t, TokenTypeEnum) else tuple(t)

    @abstractmethod
    def _parse_expr(self, **context) -> nodes.ExprNode: ...

    @abstractmethod
    def _parse_attached_code_block(
            self, *,
            opening_token: TokenTypeEnum = TokenType.Parentheses.OpenCurlyBrace,
            closing_token: TokenTypeEnum = TokenType.Parentheses.CloseCurlyBrace,
            eat_opening_token = True,
            eat_closing_token = True,
            allow_single_line_code_blocks = True,
            **context
        ) -> nodes.CodeBlockNode: ...

    @abstractmethod
    def _parse_walrus_assignment_expr(self, **context) -> nodes.ExprNode: ... 

    @abstractmethod
    def _parse_stmt(self, **context) -> nodes.StmtNode: ...

    @abstractmethod
    def _parse_primary_expr(self, **context) -> nodes.ExprNode: ...

    @abstractmethod
    def _parse_assignment_pattern(self, ending_tokens: TokenTypeSequence, **context) -> list[nodes.ExprNode]: ...

    @abstractmethod
    def _parse_unary_expr(self, **context) -> nodes.UnaryNode | nodes.ExprNode: ...
