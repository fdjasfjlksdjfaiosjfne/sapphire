import typing

from backend import errors
from parser.lexer import Token, TokenType
import parser.nodes as Nodes


class Loops:
    def peek(self, offset: int = 0) -> Token: ...
    def advance_matchings(self, ts: typing.Sequence[TokenType] = []): ...
    def advance(
        self, 
        ts: typing.Sequence[TokenType] = [], 
        error: errors.SapphireError | None = None
    ) -> Token: ...
    def parse_expr(self, **context) -> Nodes.ExprNode: ...
    def parse_attached_code_block(
            self, *,
            opening_token = TokenType.OpenCurlyBrace,
            closing_token = TokenType.CloseCurlyBrace,
            eat_opening_token = True,
            eat_closing_token = True,
            allow_single_line_code_blocks = True,
            **context
        ) -> Nodes.CodeBlockNode: ...
    def parse_while_stmt(self, **context) -> Nodes.WhileLoopNode:
        self.advance([TokenType.While])
        cond = self.parse_expr(**context)
        code = self.parse_attached_code_block(**context)
        els = None
        # $ Check for an `else` attachment
        if self.peek().type == TokenType.Else:
            self.advance([TokenType.Else])
            els = self.parse_attached_code_block(**context)
        return Nodes.WhileLoopNode(cond, code, els)

    def parse_for_stmt(self, **context) -> Nodes.ForLoopNode:
        self.advance([TokenType.For])
        # & Not my proudest work...
        syntax_expr = self.parse_expr(allow_implicit_tuples = True, **context)
        iter_vars = []
        iterable = None

        if isinstance(syntax_expr, Nodes.BinaryNode) and syntax_expr.oper == TokenType.In:
            if isinstance(syntax_expr.left, Nodes.IdentifierNode):
                iter_vars = [syntax_expr.left.symbol]
                iterable = syntax_expr.right
            elif isinstance(syntax_expr.left, Nodes.TupleNode):
                if all(isinstance(i, Nodes.IdentifierNode) for i in syntax_expr.left.value):
                    values = typing.cast(list[Nodes.IdentifierNode], syntax_expr.left.value)
                    iter_vars = [i.symbol for i in values]
                    iterable = syntax_expr.right
                else:
                    raise errors.SyntaxError("Expected only identifiers on the left-hand side of 'in'")
            else:
                raise errors.SyntaxError("Invalid iterable unpacking target before 'in'")

        elif isinstance(syntax_expr, Nodes.TupleNode):
            if not syntax_expr.value:
                raise errors.SyntaxError("Empty tuple is not valid in a for loop")
            
            *left, last = syntax_expr.value
            if (
                isinstance(last, Nodes.BinaryNode) and last.oper == TokenType.In and
                isinstance(last.left, Nodes.IdentifierNode) and
                all(isinstance(i, Nodes.IdentifierNode) for i in left)
            ):
                left = typing.cast(list[Nodes.IdentifierNode], left)
                iter_vars = [i.symbol for i in left] + [last.left.symbol]
                iterable = last.right
            else:
                raise errors.SyntaxError("Could not resolve iterable expression from tuple pattern")

        else:
            raise errors.SyntaxError("Invalid syntax in 'for' loop head")

        # ^ Sane part
        code_block = self.parse_attached_code_block(**context)
        else_block = None
        if self.peek().type == TokenType.Else:
            self.advance()
            else_block = self.parse_attached_code_block(**context)
        return Nodes.ForLoopNode(iter_vars, iterable, code_block, else_block)

    def parse_cfor_stmt(self, **context) -> Nodes.GlorifiedWhileLoopNode:
        init = None
        cond = None
        repeat = None
        els = None
        
        self.advance([TokenType.Cfor])
        self.advance([TokenType.OpenParenthesis], errors.SyntaxError(
            "Expecting a '('"
        ))
        self.advance_matchings([TokenType.NewLine])
        if self.peek().type != TokenType.Semicolon:
            init = self.parse_expr(**context)
        self.advance_matchings([TokenType.NewLine])
        self.advance([TokenType.Semicolon], errors.SyntaxError(
            "Expecting a ';'"
        ))

        self.advance_matchings([TokenType.NewLine])
        if self.peek().type != TokenType.Semicolon:
            cond = self.parse_expr(**context)
        self.advance_matchings([TokenType.NewLine])
        self.advance([TokenType.Semicolon], errors.SyntaxError(
            "Expecting a ';'"
        ))

        self.advance_matchings([TokenType.NewLine])
        if self.peek().type != TokenType.Semicolon:
            repeat = self.parse_expr(**context)
        self.advance_matchings([TokenType.NewLine])
        self.advance([TokenType.CloseParenthesis], errors.SyntaxError(
            "Expecting a ')'"
        ))

        code = self.parse_attached_code_block(**context)
        if self.peek().type == TokenType.Else:
            self.advance([TokenType.Else])
            els = self.parse_attached_code_block(**context)

        return Nodes.GlorifiedWhileLoopNode(init, cond, repeat, code, els)

    def parse_do_while_stmt(self, **context) -> Nodes.DoWhileLoopNode:
        self.advance([TokenType.Do])
        code_block = self.parse_attached_code_block()
        self.advance([TokenType.While])
        condition = self.parse_expr(**context)
        return Nodes.DoWhileLoopNode(condition, code_block)