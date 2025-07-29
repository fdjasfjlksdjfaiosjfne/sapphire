from __future__ import annotations
import typing

# ~ Used for testing purposes, when I want to run this file directly
# ~ Feel free to comment out if it cause any problems
# ~ Made by ChatGPT, might be brittle
# & Thanks for the unelegant elegant importing system, Python.
if __name__ == "__main__" and __package__ is None:
    import sys
    from pathlib import Path

    # Emulate as if we're inside the 'Sapphire' folder
    sapphire_root = Path(__file__).resolve().parent.parent.parent.parent
    sys.path.insert(0, str(sapphire_root))

    # Optional but sometimes needed to avoid relative import failures
    __package__ = "parser.parsing.exprs"

from backend import errors
from parser.lexer.lexer import Token, TokenType, Tokenizer
import parser.nodes as Nodes
from parser.parsing.exprs.sap_collections import Collections
from parser.parsing.exprs.attr_sub_call import AttributeSubcriptionCall
from parser.parsing.exprs.strs import Strings

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
## [x] 'b^'
## [x] 'b|'
## [x] '&' / 'and'
## [x] '|' / 'or'
## [x] '^' / 'xor'
## [x] Ternary Operator ('a ? b : c')
## [x] Assignment Operator (':=')
## [x] '[1, 2, 3, 4]' '{1, 2, 3, 4}' '{"a": "b"}'

class Exprs(Collections, AttributeSubcriptionCall, Strings):

    def _parse_expr(self, **context) -> Nodes.ExprNode:
        return self._parse_collections_expr(**context)

    def _parse_walrus_assignment_expr(self, **context) -> Nodes.WalrusNode | Nodes.ExprNode:
        lhs = self._parse_ternary_expr(**context)
        if self._peek().type == TokenType.SY_Walrus:
            return Nodes.WalrusNode(lhs, self._advance().value, self._parse_ternary_expr(**context))
        return lhs

    def _parse_ternary_expr(self, **context) -> Nodes.TernaryNode | Nodes.ExprNode:
        cond = self._parse_logical_expr(**context)
        if self._peek() == TokenType.SY_QuestionMark:
            self._advance()
            true_expr = self._parse_expr(**context)
            if self._peek() == TokenType.SY_GDCologne:
                self._advance()
                return Nodes.TernaryNode(cond, true_expr, self._parse_expr(**context))
            raise errors.SyntaxError("Expecting a colon")
        return cond

    # def _parse_binary_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode: ...

    def _parse_logical_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self._parse_binary_expr_using_binary_thingy(**context)
        if self._peek() in {TokenType.SY_Caret, TokenType.KW_Xor}:
            self._advance()
            return Nodes.BinaryNode(lhs, TokenType.KW_Xor, self._parse_logical_expr(**context))
        if self._peek() in {TokenType.SY_VerticalBar, TokenType.KW_Or}:
            self._advance()
            return Nodes.BinaryNode(lhs, TokenType.KW_Or, self._parse_logical_expr(**context))
        if self._peek() in {TokenType.SY_Andpersand, TokenType.KW_And}:
            self._advance()
            return Nodes.BinaryNode(lhs, TokenType.KW_And, self._parse_logical_expr(**context))
        return lhs

    def _parse_binary_expr_using_binary_thingy(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self._parse_spaceship_expr(**context)
        if self._peek() in {
            TokenType.SY_BinaryXor, 
            TokenType.SY_BinaryOr, 
            TokenType.SY_BinaryAnd, 
            TokenType.SY_LeftShift, 
            TokenType.SY_RightShift
        }:
            return Nodes.BinaryNode(lhs, self._advance().type, self._parse_binary_expr_using_binary_thingy(**context))
        return lhs

    def _parse_spaceship_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self._parse_contain_expr(**context)
        if self._peek() == TokenType.SY_Spaceship:
            return Nodes.BinaryNode(lhs, self._advance().type, self._parse_spaceship_expr(**context))
        return lhs

    def _parse_contain_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self._parse_condition_expr(**context)
        if self._peek() in {TokenType.KW_In, TokenType.KW_NotIn}:
            return Nodes.BinaryNode(lhs, self._advance().type, self._parse_contain_expr(**context))
        return lhs

    def _parse_condition_expr(self, **context) -> Nodes.ComparisonNode | Nodes.ExprNode:
        comp_tokens = frozenset([
            TokenType.SY_GreaterThan, 
            TokenType.SY_GreaterEqualThan, 
            TokenType.SY_Equal, 
            TokenType.SY_NotEqual, 
            TokenType.SY_LessEqualThan, 
            TokenType.SY_LessThan,
        ])
        lhs = self._parse_additive_expr(**context)
        if self._peek() in comp_tokens:
            comp_tokens_list = []; exprs = []
            while self._peek() in comp_tokens:
                comp_tokens_list.append(self._advance().type)
                exprs.append(self._parse_additive_expr(**context))
            return Nodes.ComparisonNode(lhs, comp_tokens_list, exprs)
        return lhs

    def _parse_additive_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self._parse_multiplicative_expr(**context)
        if self._peek() in {TokenType.SY_Plus, TokenType.SY_Minus}:
            return Nodes.BinaryNode(lhs, self._advance().type, self._parse_additive_expr(**context))
        return lhs

    def _parse_multiplicative_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self._parse_exponentiative_expr(**context)
        if self._peek() in {TokenType.SY_Asterisk, TokenType.SY_TrueDivision, TokenType.SY_FloorDivision, TokenType.SY_Modulus}:
            return Nodes.BinaryNode(lhs, self._advance().type, self._parse_multiplicative_expr(**context))
        return lhs

    def _parse_exponentiative_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self._parse_unary_expr(**context)
        if self._peek() == TokenType.SY_Exponentiation:
            return Nodes.BinaryNode(lhs, self._advance(**context).type, self._parse_exponentiative_expr(**context))
        return lhs

    def _parse_unary_expr(self, **context) -> Nodes.UnaryNode | Nodes.ExprNode:
        """
        Parses unary expressions. This include:
        - Prefix: '++', '--', '!', '~', 'not', '*', '+', '-'
        - Postfix: '++', '--'
        """
        ## Prefix
        if self._peek() in {
                TokenType.SY_Plus, TokenType.SY_Minus, TokenType.SY_Asterisk, 
                TokenType.SY_Tilda, TokenType.KW_Not, TokenType.SY_Exclamation, 
                TokenType.SY_Incre, TokenType.SY_Decre
                }:
            attachment = self._advance().type
            expr = self._parse_member_subscription_call_expr(**context)
            return Nodes.UnaryNode(attachment, expr, "Prefix")
        
        # $ At this point there should be a expression now
        # $ Time to parse it
        expr = self._parse_member_subscription_call_expr(**context)
        
        if self._peek() in {TokenType.SY_Incre, TokenType.SY_Decre}:
            return Nodes.UnaryNode(expr, self._advance().type, "Postfix")
        return expr

    def _parse_primary_expr(self, **context) -> Nodes.ExprNode:
        exclude = context.pop("exclude_create_node", [])
        token = self._advance()
        match token.type:
            case TokenType.Identifier if TokenType.Identifier not in exclude:
                return Nodes.IdentifierNode(token.value, context.pop("ident_ctx", Nodes.ExprContext.Load))
            case TokenType.PV_Int if TokenType.Identifier not in exclude:
                return Nodes.IntNode(int(token.value))
            case TokenType.PV_Float if TokenType.PV_Float not in exclude:
                return Nodes.FloatNode(float(token.value))
            case TokenType.PV_String if TokenType.PV_String not in exclude:
                return self._process_string(token.value)
            case TokenType.PV_Bool if TokenType.PV_Bool not in exclude:
                return Nodes.BoolNode(self._advance().value == "true")
            case TokenType.PV_Null if TokenType.PV_Null not in exclude:
                self._advance(); return Nodes.NullNode()
            case TokenType.PR_OpenParenthesis if TokenType.PR_OpenParenthesis not in exclude:
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
                self._advance([TokenType.PR_CloseParenthesis])
                return expr
            case _:
                raise errors.SyntaxError(f"Expecting an expression")