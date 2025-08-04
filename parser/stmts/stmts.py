import typing

from backend import errors
from parser.lexer import TokenType
import parser.nodes as Nodes
from parser.stmts.declarations import DeclarationStatements
from parser.stmts.match_case import MatchCaseStatement
from parser.stmts.loops import LoopStatements

class Stmts(MatchCaseStatement, LoopStatements, DeclarationStatements):
    def _parse_stmt(self, **context) -> Nodes.StmtNode:
        match self._peek():
            case TokenType.Statements.Declarations.MutableVariable | TokenType.Statements.Declarations.ConstantVariable:
                return self._parse_var_declaration(**context)
            case TokenType.Statements.Conditional.Condition:
                v = self._parse_if_elif_else(clause = TokenType.Statements.Conditional.Condition, **context)
                assert isinstance(v, Nodes.ConditionalNode)
                return v
            case TokenType.Statements.Loops.RunWhileCondition:
                return self._parse_while_stmt(**context)
            case TokenType.Statements.Loops.ForLoopFromPython:
                return self._parse_for_stmt(**context)
            case TokenType.Statements.Loops.ForLoopFromC:
                return self._parse_cfor_stmt(**context)
            case TokenType.Statements.Loops.StartOfDoWhileLoop:
                return self._parse_do_while_stmt(**context)
            case TokenType.Statements.Loops.PrematureExit:
                self._advance()
                # todo add label support
                return Nodes.BreakNode()
            case TokenType.Statements.Loops.SkipToNextIteration:
                # todo add label support
                self._advance()
                return Nodes.ContinueNode()
            case TokenType.Statements.ExceptionHandling.ThrowError:
                return self._parse_throw_stmt(**context)
            case TokenType.Statements.Declarations.Function:
                return self._parse_fn_declaration(**context)
            case TokenType.Statements.NewScope:
                self._advance()
                return Nodes.ScopeBlockNode(
                    self._parse_attached_code_block(**context)
                    )
            case TokenType.Statements.MatchCase.Match:
                return self._parse_match_case_stmt(**context)
            case TokenType.Statements.Return:
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
        if clause != TokenType.Statements.Conditional.Fallback:
            cond = self._parse_expr(**context)
        
        code = self._parse_attached_code_block(**context)
        
        # $ At this point, we're done with parsing the clause itself
        # $ Now we're checking on continuity

        if clause == TokenType.Statements.Conditional.Fallback:
            return code
        
        # & Yes, static type checker, I do know what am I doing
        # & Trust me
        cond = typing.cast(Nodes.ExprNode, cond)

        # ? Check if there's any other connectable clause (elif/else) behind
        
        if self.peek().type in {TokenType.Statements.Conditional.FallbackWithCondition, TokenType.Statements.Conditional.Fallback}:
            return Nodes.ConditionalNode(
                cond, code,
                self.parse_if_elif_else(clause = self.peek().type, **context))
        return Nodes.ConditionalNode(cond, code)

    def _parse_throw_stmt(self, **context) -> Nodes.ThrowNode:
        self._advance([TokenType.Statements.ExceptionHandling.ThrowError])
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
            if self._peek().type == TokenType.Statements.ExceptionHandling.SourceOfThrowingError:
                self._advance(TokenType.Statements.ExceptionHandling.SourceOfThrowingError)
                cause = self._parse_expr(**context)
        return Nodes.ThrowNode(err, cause)

    def _parse_attached_code_block(
            self, *,
            opening_token = TokenType.Parentheses.OpenCurlyBrace,
            closing_token = TokenType.Parentheses.CloseCurlyBrace,
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
                self._advance([TokenType.NewLine, TokenType.Symbols.StatementSeparator])
            
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