from typing import List, Set, Literal
from lexer.lexer import Token
from lexer.tokens import TokenType
from enum import Enum
import nodes as N

class Parser:
    class MatchingSets(Enum):
        Additive = {TokenType.Plus, TokenType.Minus}
        Multiplicative = {TokenType.Asterisk, TokenType.Divide, TokenType.Modulus}
        Comparative = {TokenType.GreaterThan, TokenType.GreaterEqualThan, TokenType.Equal, TokenType.NotEqual, TokenType.LessEqualThan, TokenType.LessThan}
        Xor = {TokenType.Caret, TokenType.Xor}
    
    @classmethod
    def produce_ast(cls, tokens: List[Token]) -> N.ProgramNode:
        cls.tokens = tokens
        program = N.ProgramNode([])
        while cls.at() != TokenType.EoF:
            cls.remove_new_lines()
            program.body.append(cls.parse_stmt())
        del cls.tokens
        return program

    @classmethod
    def at(cls) -> Token:
        return cls.tokens[0]

    @classmethod
    def eat(cls) -> Token:
        return cls.tokens.pop(0)
    
    @classmethod
    def asrt(cls, type: TokenType) -> Token:
        if (tkn := cls.eat()) != type:
            raise ValueError("e")
        return tkn
    
    @classmethod
    def remove_new_lines(cls) -> None:
        if cls.at() == TokenType.NewLine:
            cls.eat()

    @classmethod
    def parse_stmt(cls) -> N.Stmt:
        match cls.at():
            case TokenType.Fn:
                return cls.parse_fn_declaration()
            case _:
                return cls.parse_assignment_stmt()
    
    @classmethod
    def parse_assignment_stmt(cls) -> N.AssignmentNode | N.Expr:
        lhs = cls.parse_expr()
        if cls.at() @ {TokenType.AssignOper, TokenType.ModifierAssignOper}:
            return N.AssignmentNode(lhs, cls.eat().value, cls.parse_assignment_expr())
        return lhs
    
    @classmethod
    def parse_expr(cls) -> N.Expr:
        return cls.parse_assignment_expr()
    
    @classmethod
    def parse_assignment_expr(cls) -> N.WalrusExprNode | N.Expr:
        lhs = cls.parse_collections_expr()
        if cls.at() == TokenType.WalrusOper:
            return N.WalrusExprNode(lhs, cls.eat().value, cls.parse_collections_expr())
        return lhs
    
    @classmethod
    def parse_collections_expr(cls):
        match cls.at():
            case TokenType.OpenCurlyBrace:
                cls.eat()
                raise Exception()
            case TokenType.OpenSquareBracket:
                cls.eat()
                raise Exception()
            case _:
                return cls.parse_ternary_expr()
    
    @classmethod
    def parse_ternary_expr(cls) -> N.TernaryNode | N.Expr:
        cond = cls.parse_logical_expr()
        if cls.at() == TokenType.QuestionMark:
            cls.eat()
            true_expr = cls.parse_expr()
            if cls.at() == TokenType.GDCologne:
                cls.eat()
                return N.TernaryNode(cond, true_expr, cls.parse_expr())
            return N.TernaryNode(cond, true_expr, N.NullNode())
        return cond
    
    @classmethod
    def parse_logical_expr(cls) -> N.BinaryExprNode | N.Expr:
        lhs = cls.parse_condition_expr()
        if cls.at() @ cls.MatchingSets.Xor:
            return 
    
    @classmethod
    def parse_condition_expr(cls) -> N.ComparisonNode | N.Expr:
        lhs = cls.parse_additive_expr()
        if cls.at() @ cls.matching_sets["comparitive"]:
            comp_tokens = []; exprs = []
            while cls.at() @ cls.matching_sets["comparitive"]:
                comp_tokens.append(cls.eat().type)
                exprs.append(cls.parse_additive_expr())
            return N.ComparisonNode(lhs, comp_tokens, exprs)
        return lhs
    
    @classmethod
    def parse_additive_expr(cls) -> N.BinaryExprNode | N.Expr:
        lhs = cls.parse_multiplicative_expr()
        if cls.at() @ cls.matching_sets["additive"]:
            return N.Binarynd.ExprNode(lhs, cls.eat().type, cls.parse_additive_expr())
        return lhs
    
    @classmethod
    def parse_multiplicative_expr(cls) -> N.BinaryExprNode | N.Expr:
        lhs = cls.parse_exponentiative_expr()
        if cls.at() @ cls.matching_sets["multiplicative"]:
            return N.Binarynd.ExprNode(lhs, cls.eat().type, cls.parse_multiplicative_expr())
        return lhs
    
    @classmethod
    def parse_exponentiative_expr(cls) -> N.BinaryExprNode | N.Expr:
        lhs = cls.parse_primary_expr()
        if cls.at() == TokenType.Exponentiation:
            return N.Binarynd.ExprNode(lhs, cls.eat().type, cls.parse_exponentiative_expr())
        return lhs
    
    @classmethod
    def parse_primary_expr(
        cls, 
        exclude: Set[
            Literal[
                TokenType.Identifier,
                TokenType.Int,
                TokenType.Float,
                TokenType.Str,
                TokenType.Bool,
                TokenType.Null,
                TokenType.OpenParenthesis
            ]
        ] = {}
        ) -> N.IntNode | N.FloatNode | N.StrNode | N.BoolNode | N.NullNode | N.IdentifierNode | N.Expr:
        match cls.at().type:
            case TokenType.Identifier if TokenType.Identifier not in exclude:
                return N.IdentifierNode(cls.eat().value)
            case TokenType.Int if TokenType.Int not in exclude:
                return N.IntNode(int(cls.eat().value))
            case TokenType.Float if TokenType.Float not in exclude:
                return N.FloatNode(float(cls.eat().value))
            case TokenType.Str if TokenType.Str not in exclude:
                return N.StrNode(cls.eat().value)
            case TokenType.Bool if TokenType.Bool not in exclude:
                return N.BoolNode(True if cls.eat().value == "true" else False)
            case TokenType.Null if TokenType.Null not in exclude:
                cls.eat()
                return N.NullNode()
            case TokenType.OpenParenthesis if TokenType.OpenParenthesis not in exclude:
                cls.eat()
                cls.remove_new_lines()
                expr = cls.parse_expr()
                cls.remove_new_lines()
                cls.asrt(TokenType.CloseParenthesis)
                return expr
            case _:
                raise Exception(cls.tokens)