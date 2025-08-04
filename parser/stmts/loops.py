import itertools
import typing

from backend import errors
from parser.lexer import TokenType, Loops, Parentheses
import parser.nodes as Nodes
from parser.core import ParserNamespaceSkeleton

class LoopStatements(ParserNamespaceSkeleton):
    def _parse_while_stmt(self, **context) -> Nodes.WhileLoopNode:
        self._advance([Loops.RunWhileCondition])
        cond = self._parse_expr(**context)
        code = self._parse_attached_code_block(**context)
        els = None
        # $ Check for an `else` attachment
        if self._peek().type == Loops.UninterruptedLoopExecution:
            self._advance([Loops.UninterruptedLoopExecution])
            els = self._parse_attached_code_block(**context)
        return Nodes.WhileLoopNode(cond, code, els)

    def _parse_for_stmt(self, **context) -> Nodes.ForLoopNode:
        self._advance(Loops.ForLoopFromPython)

        assignment = self._parse_assignment_pattern(ending_tokens = Loops.IterableVarsAndIterableSeparatorInForLoopFromPython)
        iter_vars = [i.symbol for i in assignment if isinstance(i, Nodes.IdentifierNode)]
        if len(assignment) != len(iter_vars):
            raise errors.SyntaxError("Invalid syntax")
        self._advance(Loops.IterableVarsAndIterableSeparatorInForLoopFromPython)
        iterable = self._parse_expr(**context)
        code_block = self._parse_attached_code_block(**context)
        else_block = None
        if self._peek().type == Loops.UninterruptedLoopExecution:
            self._advance(Loops.UninterruptedLoopExecution)
            else_block = self._parse_attached_code_block()
        
        return Nodes.ForLoopNode(iter_vars, iterable, code_block, else_block)

    def _parse_cfor_stmt(self, **context) -> Nodes.GlorifiedWhileLoopNode:
        init = None
        cond = None
        repeat = None
        els = None
        
        self._advance([Loops.ForLoopFromC])
        self._advance([Parentheses.OpenParenthesis], errors.SyntaxError(
            "Expecting a '('"
        ))
        self._advance_matchings([TokenType.NewLine])
        if self._peek().type != TokenType.Symbols.ForLoopFromCArgumentSeparator:
            init = self._parse_expr(**context)
        self._advance_matchings([TokenType.NewLine])
        self._advance([TokenType.Symbols.ForLoopFromCArgumentSeparator], errors.SyntaxError(
            "Expecting a ';'"
        ))

        self._advance_matchings([TokenType.NewLine])
        if self._peek().type != TokenType.Symbols.ForLoopFromCArgumentSeparator:
            cond = self._parse_expr(**context)
        self._advance_matchings([TokenType.NewLine])
        self._advance([TokenType.Symbols.ForLoopFromCArgumentSeparator], errors.SyntaxError(
            "Expecting a ';'"
        ))

        self._advance_matchings([TokenType.NewLine])
        if self._peek().type != TokenType.Symbols.ForLoopFromCArgumentSeparator:
            repeat = self._parse_expr(**context)
        self._advance_matchings([TokenType.NewLine])
        self._advance([Parentheses.CloseParenthesis], errors.SyntaxError(
            "Expecting a ')'"
        ))

        code = self._parse_attached_code_block(**context)
        if self._peek().type == Loops.UninterruptedLoopExecution:
            self._advance([Loops.UninterruptedLoopExecution])
            els = self._parse_attached_code_block(**context)

        return Nodes.GlorifiedWhileLoopNode(init, cond, repeat, code, els)

    def _parse_do_while_stmt(self, **context) -> Nodes.DoWhileLoopNode:
        self._advance([Loops.StartOfDoWhileLoop])
        code_block = self._parse_attached_code_block()
        self._advance([Loops.ConditionOfDoWhileLoop])
        condition = self._parse_expr(**context)

        els = None
        if self._peek().type == Loops.UninterruptedLoopExecution:
            self._advance([Loops.UninterruptedLoopExecution])
            els = self._parse_attached_code_block(**context)
        return Nodes.DoWhileLoopNode(condition, code_block, els)