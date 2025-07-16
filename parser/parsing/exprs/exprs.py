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
from parser.lexer import Token, TokenType, Tokenizer
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
    tokens: Tokenizer
    def advance_matchings(self, ts: typing.Sequence[TokenType] = []): ...
    def peek(self, offset: int = 0) -> Token: ...
    def parse_expr(self, **context) -> Nodes.ExprNode:
        return self.parse_collections_expr(**context)

    def parse_assignment_expr(self, **context) -> Nodes.WalrusNode | Nodes.ExprNode:
        lhs = self.parse_ternary_expr(**context)
        if self.peek().type == TokenType.WalrusOper:
            return Nodes.WalrusNode(lhs, self.advance().value, self.parse_ternary_expr(**context))
        return lhs

    def parse_ternary_expr(self, **context) -> Nodes.TernaryNode | Nodes.ExprNode:
        cond = self.parse_logical_expr(**context)
        if self.peek() == TokenType.QuestionMark:
            self.advance()
            true_expr = self.parse_expr(**context)
            if self.peek() == TokenType.GDCologne:
                self.advance()
                return Nodes.TernaryNode(cond, true_expr, self.parse_expr(**context))
            raise errors.SyntaxError("Expecting a colon")
        return cond

    def parse_logical_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self.parse_binary_expr(**context)
        if self.peek() in {TokenType.Caret, TokenType.Xor}:
            self.advance()
            return Nodes.BinaryNode(lhs, TokenType.Xor, self.parse_logical_expr(**context))
        if self.peek() in {TokenType.VerticalBar, TokenType.Or}:
            self.advance()
            return Nodes.BinaryNode(lhs, TokenType.Or, self.parse_logical_expr(**context))
        if self.peek() in {TokenType.Andpersand, TokenType.And}:
            self.advance()
            return Nodes.BinaryNode(lhs, TokenType.And, self.parse_logical_expr(**context))
        return lhs

    def parse_binary_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self.parse_spaceship_expr(**context)
        if self.peek() in {
            TokenType.BinaryXor, 
            TokenType.BinaryOr, 
            TokenType.BinaryAnd, 
            TokenType.LeftShift, 
            TokenType.RightShift
        }:
            return Nodes.BinaryNode(lhs, self.advance().type, self.parse_binary_expr(**context))
        return lhs

    def parse_spaceship_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self.parse_contain_expr(**context)
        if self.peek() == TokenType.Spaceship:
            return Nodes.BinaryNode(lhs, self.advance().type, self.parse_spaceship_expr(**context))
        return lhs

    def parse_contain_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self.parse_condition_expr(**context)
        if self.peek() in {TokenType.In, TokenType.NotIn}:
            return Nodes.BinaryNode(lhs, self.advance().type, self.parse_contain_expr(**context))
        return lhs

    def parse_condition_expr(self, **context) -> Nodes.ComparisonNode | Nodes.ExprNode:
        comp_tokens = frozenset([
            TokenType.GreaterThan, 
            TokenType.GreaterEqualThan, 
            TokenType.Equal, 
            TokenType.NotEqual, 
            TokenType.LessEqualThan, 
            TokenType.LessThan,
        ])
        lhs = self.parse_additive_expr(**context)
        if self.peek() in comp_tokens:
            comp_tokens_list = []; exprs = []
            while self.peek() in comp_tokens:
                comp_tokens_list.append(self.advance().type)
                exprs.append(self.parse_additive_expr(**context))
            return Nodes.ComparisonNode(lhs, comp_tokens_list, exprs)
        return lhs

    def parse_additive_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self.parse_multiplicative_expr(**context)
        if self.peek() in {TokenType.Plus, TokenType.Minus}:
            return Nodes.BinaryNode(lhs, self.advance().type, self.parse_additive_expr(**context))
        return lhs

    def parse_multiplicative_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self.parse_exponentiative_expr(**context)
        if self.peek() in {TokenType.Asterisk, TokenType.TrueDivision, TokenType.FloorDivision, TokenType.Modulus}:
            return Nodes.BinaryNode(lhs, self.advance().type, self.parse_multiplicative_expr(**context))
        return lhs

    def parse_exponentiative_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        lhs = self.parse_unary_expr(**context)
        if self.peek() == TokenType.Exponentiation:
            return Nodes.BinaryNode(lhs, self.advance(**context).type, self.parse_exponentiative_expr(**context))
        return lhs

    def parse_unary_expr(self, **context) -> Nodes.UnaryNode | Nodes.ExprNode:
        """
        Parses unary expressions. This include:
        - Prefix: '++', '--', '!', '~', 'not', '*', '+', '-'
        - Postfix: '++', '--'
        """
        ## Prefix
        if self.peek() in {
                TokenType.Plus, TokenType.Minus, TokenType.Asterisk, 
                TokenType.Tilda, TokenType.Not, TokenType.Exclamation, 
                TokenType.Incre, TokenType.Decre
                }:
            attachment = self.advance().type
            expr = self.parse_member_subscription_call_expr(**context)
            return Nodes.UnaryNode(attachment, expr, "Prefix")
        
        # $ At this point there should be a expression now
        # $ Time to parse it
        expr = self.parse_member_subscription_call_expr(**context)
        
        if self.peek() in {TokenType.Incre, TokenType.Decre}:
            return Nodes.UnaryNode(expr, self.advance().type, "Postfix")
        return expr

    def parse_primary_expr(self, **context) -> Nodes.ExprNode:
        exclude = context.pop("exclude_create_node", [])
        token = self.advance()
        match token.type:
            case TokenType.Identifier if TokenType.Identifier not in exclude:
                return Nodes.IdentifierNode(token.value, context.pop("ident_ctx", Nodes.ExprContext.Load))
            case TokenType.Int if TokenType.Identifier not in exclude:
                return Nodes.IntNode(int(token.value))
            case TokenType.Float if TokenType.Float not in exclude:
                return Nodes.FloatNode(float(token.value))
            case TokenType.Str if TokenType.Str not in exclude:
                return self.process_string(token.value)
            case TokenType.Bool if TokenType.Bool not in exclude:
                return Nodes.BoolNode(self.advance().value == "true")
            case TokenType.Null if TokenType.Null not in exclude:
                self.advance(); return Nodes.NullNode()
            case TokenType.OpenParenthesis if TokenType.OpenParenthesis not in exclude:
                self.advance()
                while self.peek() == TokenType.NewLine:
                    self.advance([TokenType.NewLine])
                expr = self.parse_expr(
                    in_parentheses = True,
                    allow_explicit_tuple = True,
                    **context
                )
                while self.peek() == TokenType.NewLine:
                    self.advance([TokenType.NewLine])
                self.advance([TokenType.CloseParenthesis])
                return expr
            case _:
                raise errors.SyntaxError(f"Expecting an expression")