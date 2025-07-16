import typing
from backend import errors
import parser.nodes as Nodes
from parser.lexer import TokenType, Tokenizer, Token

class MatchCase:
    tokens: Tokenizer
    def peek(self, offset: int = 0) -> Token: ...
    def advance(
        self, 
        ts: typing.Sequence[TokenType] = [], 
        error: errors.SapphireError | None = None
    ) -> Token: ...
    def parse_attached_code_block(
            self, *,
            opening_token = TokenType.OpenCurlyBrace,
            closing_token = TokenType.CloseCurlyBrace,
            eat_opening_token = True,
            eat_closing_token = True,
            allow_single_line_code_blocks = True,
            **context
        ) -> Nodes.CodeBlockNode: ...
    def parse_expr(self, **context) -> Nodes.ExprNode: ...

    def parse_match_case_stmt(self, **context) -> Nodes.MatchCaseNode:
        self.advance([TokenType.Match])
        subject = self.parse_expr(**context)
        self.advance([TokenType.OpenCurlyBrace])
        cases = []
        while self.peek().type != TokenType.CloseCurlyBrace:
            cases.append(self.parse_case_stmt(**context))
        self.advance([TokenType.CloseCurlyBrace])
        return Nodes.MatchCaseNode(subject, cases)

    def parse_case_stmt(self, **context) -> Nodes.CaseNode:
        self.advance([TokenType.Case])
        guard = None
        pattern = self.parse_match_pattern(**context)
        if self.peek().type == TokenType.If:
            self.advance([TokenType.If], error = errors.InternalError(
                "A redundant check for the 'if' token has been tripped\n"
                "Location: MatchCase.parse_case_stmt()"
            ))
            guard = self.parse_expr(**context)

        body = self.parse_attached_code_block(
            opening_token = TokenType.GDCologne,
            closing_token = TokenType.Case,
            eat_closing_token = False,
            allow_single_line_code_blocks = True,
            **context
        )
        return Nodes.CaseNode(pattern, guard, body)

    def parse_match_pattern(self, **context) -> Nodes.MatchPatternNode:
        ...