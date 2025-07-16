import typing

from backend import errors
from parser.lexer import Token, TokenType, Tokenizer
import parser.nodes as Nodes
from parser.parsing.stmts.match_case import MatchCase
from parser.parsing.stmts.loops import Loops

class Stmts(MatchCase, Loops):
    tokens: Tokenizer
    def advance(
        self, 
        ts: typing.Sequence[TokenType] = [], 
        error: errors.SapphireError | None = None
    ) -> Token: ...
    def peek(self, offset: int = 0) -> Token: ...
    def parse_stmt(self, **context) -> Nodes.StmtNode:
        match self.peek():
            case TokenType.Let | TokenType.Const:
                return self.parse_var_declaration(**context)
            case TokenType.If:
                v = self.parse_if_elif_else(clause = TokenType.If, **context)
                assert isinstance(v, Nodes.ConditionalNode)
                return v
            case TokenType.While:
                return self.parse_while_stmt(**context)
            case TokenType.For:
                return self.parse_for_stmt(**context)
            case TokenType.Cfor:
                return self.parse_cfor_stmt(**context)
            case TokenType.Do:
                return self.parse_do_while_stmt(**context)
            case TokenType.Break:
                # todo add label support
                return Nodes.BreakNode()
            case TokenType.Continue:
                # todo add label support
                return Nodes.ContinueNode()
            case TokenType.Throw:
                return self.parse_throw_stmt()
            case TokenType.Scope:
                self.advance()
                return Nodes.ScopeBlockNode(
                    self.parse_attached_code_block(**context)
                    )
            case TokenType.Match:
                return self.parse_match_case_stmt(**context)
            case TokenType.Return:
                self.advance()
                return Nodes.ReturnNode(
                    self.parse_expr(allow_implicit_tuples = True, **context)
                )
            case _:
                return self.parse_assignment_stmt(**context)

    def parse_var_declaration(self, **context) -> Nodes.VarDeclarationNode:
        constant = self.advance() == TokenType.Const
        names = self.parse_expr(allow_implicit_tuples = True, **context)
        if self.peek() == TokenType.AssignOper:
            self.advance()
            value = self.parse_expr(allow_implicit_tuples = True, **context)
        else:
            value = None
        return Nodes.VarDeclarationNode(name, value, constant) # type: ignore

    def parse_if_elif_else(self, **context):
        try:
            clause = context.pop("clause")
        except KeyError:
            raise errors.InternalError(
                f"'clause' is not being passed into 'parse_if_elif_else()' from {__package__}"
            )
        self.advance(clause)
        cond = None

        if clause != TokenType.Else:
            cond = self.parse_expr(**context)
        
        code = self.parse_attached_code_block(**context)
        
        # $ At this point, we're done with parsing the clause itself
        # $ Now we're checking on continuity
        
        # ? This checks on the `else`
        # ? If it is, just return the code block
        # ? Without any attempt at continuation
        if clause == TokenType.Else:
            return code

        # $ At this point, the block we're parsing should be a if/elif block
        # $ Since they can be connected with another elif or else clause
        # $ Continue to look for it

        # ? Check if there's any other connectable clause (elif/else) behind
        if self.peek().type in {TokenType.Elif, TokenType.Else}:
            
            return Nodes.ConditionalNode(
                cond, code,
                self.parse_if_elif_else(clause = self.peek().type, **context))
        return Nodes.ConditionalNode(cond, code)

    def parse_throw_stmt(self, **context) -> Nodes.ThrowNode:
        self.advance([TokenType.Throw])
        err = None
        cause = None
        
        save_point = self.tokens.save()
        try:
            err = self.parse_expr(**context)
        except errors.SapphireError:
            # & FIND ERROR EXPRESSION FAILED. BACK OFF.
            # $ If the expression is wrong, it'll know next time it parses it
            self.tokens.load(save_point)
        else:
            if ...:
                ...
        return Nodes.ThrowNode(err, cause)

    def parse_assignment_stmt(self, **context) -> Nodes.AssignmentNode | Nodes.ModifierAssignmentNode | Nodes.ExprNode:
        # @ This probably needs a makeover
        # TODO
        lhs = self.parse_expr(**context)
        match self.peek().type:
            case TokenType.AssignOper:
                exprs = [lhs]
                while self.peek().type == TokenType.AssignOper:
                    self.advance()
                    exprs.append(self.parse_expr(**context))
                return Nodes.AssignmentNode(exprs)
            case TokenType.ModifierAssignOper:
                return Nodes.ModifierAssignmentNode(lhs, self.advance().value, self.parse_expr(**context))
        return lhs

    def parse_attached_code_block(
            self, *,
            opening_token = TokenType.OpenCurlyBrace,
            closing_token = TokenType.CloseCurlyBrace,
            eat_opening_token = True,
            eat_closing_token = True,
            allow_single_line_code_blocks = True,
            **context
        ) -> Nodes.CodeBlockNode:
        # ^ Create a code block
        code = Nodes.CodeBlockNode()
        # $ If the code block uses {}
        if self.peek().type == opening_token:
            if eat_opening_token:
                self.advance([opening_token])
            
            # Do-while loop
            while True:
                code.append(self.parse_stmt(**context))
                if self.peek().type == closing_token:
                    break
                self.advance([TokenType.NewLine, TokenType.Semicolon])
            
            if eat_closing_token:
                self.advance([closing_token])
            elif self.peek().type != closing_token:
                raise errors.SyntaxError("The code block is not closed")
        elif allow_single_line_code_blocks:
            # $ The code block doesn't use {}
            code.append(self.parse_stmt(**context))
        else:
            raise errors.SyntaxError("Expecting a code block")
        return code