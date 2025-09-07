from __future__ import annotations
import typing

# ~ Used for testing purposes, when I want to run this file directly
# ~ Feel free to comment out if it cause any problems
# ~ Made by ChatGPT, might be brittle
# & Thanks for the unelegant elegant importing system, Python.
# if __name__ == "__main__" and __package__ is None:
#     import sys
#     from pathlib import Path

#     # Emulate as if we're inside the 'Sapphire' folder
#     sapphire_root = Path(__file__).resolve().parent.parent.parent.parent
#     sys.path.insert(0, str(sapphire_root))

#     # Optional but sometimes needed to avoid relative import failures
#     __package__ = "parser.parsing.exprs"

from backend import errors
from lexer import TokenType, UnaryOperators, TernaryOperators
import parser.nodes as Nodes
from backend.config import CONFIG
from parser.exprs.sap_collections import Collections
from parser.exprs.attr_sub_call import AttributeSubcriptionCall
from parser.exprs.strs import Strings
from parser.exprs.binops import BinaryOperations

# ^ The order of precendence, the top being the one that is processed first
# Note that the last will be called first
## [x] PARENTHESES ()
## [x] PrimaryExpr (int, float, string, etc.)
## [x] 'Subscription[]', 'member.access', 'Call()'
## [x] Unary Operators ('!', 'not', '~', '-', '+', '*' | '++', '--')
## [x] '**'
## [x] '*' / '/' / '//' / '%'
## [x] '+' / '-'
## [] '|>'
## [x] 'in' / 'not in'
## [x] '<' / '>' / '>=' / '<=' / '==' / '!='
## [x] '<=>'
## [x] '<<' / '>>'
## [x] 'b&'
## [x] 'b|'
## [x] 'b^'
## [x] '&' / 'and'
## [x] '|' / 'or'
## [x] '^' / 'xor'
## [x] Ternary Operator ('a ? b : c')
## [x] Assignment Operator (':=')
## [x] '[1, 2, 3, 4]' '{1, 2, 3, 4}' '{"a": "b"}'

class Exprs(Collections, BinaryOperations, AttributeSubcriptionCall, Strings):

    def _parse_expr(self, **context) -> Nodes.ExprNode:
        return self._parse_collections_expr(**context)

    def _parse_walrus_assignment_expr(self, **context) -> Nodes.WalrusNode | Nodes.ExprNode:
        lhs = self._parse_ternary_expr(**context)
        if self._peek().type == TokenType.Symbols.WalrusOper:
            self._advance().value
            return Nodes.WalrusNode(lhs, self._parse_ternary_expr(**context))
        return lhs
    
    def _parse_ternary_expr(self, **context) -> Nodes.TernaryNode | Nodes.ExprNode:
        cond = self._parse_logical_xor_expr(**context)
        if self._peek() == TernaryOperators.ConditionSeparator:
            self._advance()
            true_expr = self._parse_expr(**context)
            if self._peek() == TernaryOperators.ResultSeparator:
                self._advance()
                return Nodes.TernaryNode(cond, true_expr, self._parse_expr(**context))
            raise errors.SyntaxError("Expecting a colon")
        return cond

    def _parse_unary_expr(self, **context) -> Nodes.UnaryNode | Nodes.ExprNode:
        """
        Parses unary expressions. This include:
        - Prefix: '++', '--', '!', '~', 'not', '*', '+', '-'
        - Postfix: '++', '--'
        """
        ## Prefix
        if self._peek() in (
                UnaryOperators.Positive, UnaryOperators.Negative, 
                UnaryOperators.BinaryInversion, UnaryOperators.LogicalNot, 
                UnaryOperators.HybridNot, UnaryOperators.Increment, UnaryOperators.Decrement,
                UnaryOperators.PositionalUnpack, UnaryOperators.KeywordUnpack
            ):
            attachment = self._advance().type
            expr = self._parse_member_subscription_call_expr(**context)
            return Nodes.UnaryNode(expr, attachment, "Prefix")
        
        # $ At this point there should be a expression now
        # $ Time to parse it
        expr = self._parse_member_subscription_call_expr(**context)
        
        if self._peek() in (UnaryOperators.Increment, UnaryOperators.Decrement):
            return Nodes.UnaryNode(expr, self._advance().type, "Postfix")
        return expr

    def _parse_primary_expr(self, **context) -> Nodes.ExprNode:
        exclude = context.pop("exclude_create_node", [])
        token = self._advance()
        match token.type:
            case TokenType.Identifier if TokenType.Identifier not in exclude:
                return Nodes.IdentifierNode(token.value, context.pop("ident_ctx", Nodes.ExprContext.Load))
            case TokenType.Primitives.Int if TokenType.Primitives.Int not in exclude:
                return Nodes.IntNode(int(token.value, base = 0))
            case TokenType.Primitives.Float if TokenType.Primitives.Float not in exclude:
                return Nodes.FloatNode(float(token.value))
            case TokenType.Primitives.String if TokenType.Primitives.String not in exclude:
                return self._process_string(token.value)
            case TokenType.Primitives.Boolean if TokenType.Primitives.Boolean not in exclude:
                return Nodes.BoolNode(self._advance().value == "true")
            case TokenType.Primitives.Null if TokenType.Primitives.Null not in exclude:
                self._advance(); return Nodes.NullNode()
            case TokenType.Parentheses.OpenParenthesis if TokenType.Parentheses.OpenParenthesis not in exclude:
                self._advance()
                while self._peek() == TokenType.NewLine:
                    self._advance([TokenType.NewLine])
                expr = self._parse_expr(
                    in_parentheses = True,
                    allow_explicit_tuple = True,
                    **context
                )
                while self._peek() == TokenType.NewLine:
                    self._advance([TokenType.NewLine])
                self._advance([TokenType.Parentheses.CloseParenthesis])
                return expr
            case _:
                raise errors.SyntaxError(f"Expecting an expression")