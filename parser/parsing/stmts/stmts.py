import typing

from backend import errors
from parser.lexer.lexer import Token, TokenType, Tokenizer
import parser.nodes as Nodes
from parser.parsing.stmts.declarations import Declarations
from parser.parsing.stmts.match_case import MatchCase
from parser.parsing.stmts.loops import Loops

class Stmts(MatchCase, Loops, Declarations):
    def _parse_stmt(self, **context) -> Nodes.StmtNode:
        match self._peek():
            case TokenType.KW_Let | TokenType.KW_Const:
                return self._parse_var_declaration(**context)
            case TokenType.KW_If:
                v = self._parse_if_elif_else(clause = TokenType.KW_If, **context)
                assert isinstance(v, Nodes.ConditionalNode)
                return v
            case TokenType.KW_WhileLoop:
                return self._parse_while_stmt(**context)
            case TokenType.KW_PythonFor:
                return self._parse_for_stmt(**context)
            case TokenType.KW_CFor:
                return self._parse_cfor_stmt(**context)
            case TokenType.KW_DoWhileLoop:
                return self._parse_do_while_stmt(**context)
            case TokenType.KW_Break:
                # todo add label support
                return Nodes.BreakNode()
            case TokenType.KW_Continue:
                # todo add label support
                return Nodes.ContinueNode()
            case TokenType.KW_Throw:
                return self._parse_throw_stmt(**context)
            case TokenType.KW_FunctionDeclaration:
                return self._parse_fn_declaration(**context)
            case TokenType.KW_Scope:
                self._advance()
                return Nodes.ScopeBlockNode(
                    self._parse_attached_code_block(**context)
                    )
            case TokenType.KW_Match:
                return self._parse_match_case_stmt(**context)
            case TokenType.KW_Return:
                self._advance()
                return Nodes.ReturnNode(
                    self._parse_expr(allow_implicit_tuples = True, **context)
                )
            case _:
                return self._parse_assignment_stmt(**context)



    def _parse_if_elif_else(self, **context):
        try:
            clause = context.pop("clause")
        except KeyError:
            raise errors.InternalError(
                f"'clause' is not being passed into 'parse_if_elif_else()' from {__package__}"
            )
        self._advance()
        
        cond = None
        if clause != TokenType.KW_Else:
            cond = self._parse_expr(**context)
        
        code = self._parse_attached_code_block(**context)
        
        # $ At this point, we're done with parsing the clause itself
        # $ Now we're checking on continuity

        if clause == TokenType.KW_Else:
            return code
        
        # & Yes, static type checker, I do know what am I doing
        # & Trust me
        cond = typing.cast(Nodes.ExprNode, cond)

        # ? Check if there's any other connectable clause (elif/else) behind
        
        if self.peek().type in {TokenType.KW_ElseIf, TokenType.KW_Else}:
            return Nodes.ConditionalNode(
                cond, code,
                self.parse_if_elif_else(clause = self.peek().type, **context))
        return Nodes.ConditionalNode(cond, code)

    def _parse_throw_stmt(self, **context) -> Nodes.ThrowNode:
        self._advance([TokenType.KW_Throw])
        err = None
        cause = None
        
        save_point = self.tokens.save()
        try:
            err = self._parse_expr(**context)
        except errors.SapphireError:
            # & FIND ERROR EXPRESSION FAILED. BACK OFF.
            # $ If the expression is wrong, it'll know next time it parses it
            self.tokens.load(save_point)
        else:
            if self._peek().type == TokenType.KW_From:
                self._advance(TokenType.KW_From)
                cause = self._parse_expr(**context)
        return Nodes.ThrowNode(err, cause)

    def _parse_attached_code_block(
            self, *,
            opening_token = TokenType.PR_OpenCurlyBrace,
            closing_token = TokenType.PR_CloseCurlyBrace,
            eat_opening_token = True,
            eat_closing_token = True,
            allow_single_line_code_blocks = True,
            **context
        ) -> Nodes.CodeBlockNode:

        code = Nodes.CodeBlockNode()
        # $ If the code block uses {}
        if self._peek().type == opening_token:
            if eat_opening_token:
                self._advance([opening_token])
            
            # Do-while loop
            while True:
                code.append(self._parse_stmt(**context))
                if self._peek().type == closing_token:
                    break
                self._advance([TokenType.NewLine, TokenType.SY_Semicolon])
            
            if eat_closing_token:
                self._advance([closing_token])
            elif self._peek().type != closing_token:
                raise errors.SyntaxError("The code block is not closed")
        elif allow_single_line_code_blocks:
            # $ The code block doesn't use {}
            code.append(self._parse_stmt(**context))
        else:
            raise errors.SyntaxError("Expecting a code block")
        return code