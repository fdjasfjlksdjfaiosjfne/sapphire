from typing import *
from lexer.lexer import Token
from lexer.tokens import TokenType
from .nodes import *

class Parser:
    @classmethod
    def produce_ast(cls, tokens: List[Token]) -> ProgramNode:
        cls.tokens = tokens
        program = ProgramNode([])
        while cls.at() != TokenType.EoF:
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
    def parse_stmt(cls) -> Stmt:
        match cls.at():
            case TokenType.Fn:
                return cls.parse_fn_declaration()
            case _:
                return cls.parse_assignment_stmt()
    
    @classmethod
    def parse_assignment_stmt(cls) -> AssignmentNode | Expr:
        lhs = cls.parse_assignment_expr()
        if cls.at() == TokenType.AssignOper:
            return AssignmentNode(lhs, cls.eat().value, cls.parse_assignment_expr())
        return lhs
    
    @classmethod
    def parse_expr(cls) -> Expr:
        return cls.parse_assignment_expr()
    
    @classmethod
    def parse_assignment_expr(cls):
        lhs = cls.parse_collections_expr()
        if cls.at() == TokenType.WalrusOper:
            return WalrusExprNode(lhs, cls.eat().value, cls.parse_collections_expr())
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
                return cls.parse_additive_expr()
    
    @classmethod
    def parse_additive_expr(cls) -> BinaryExprNode | Expr:
        lhs = cls.parse_multiplicative_expr()
        if cls.at()._in(TokenType.Plus, TokenType.Minus):
            return BinaryExprNode(lhs, cls.eat().type, cls.parse_additive_expr())
        return lhs
    
    @classmethod
    def parse_multiplicative_expr(cls) -> BinaryExprNode | Expr:
        lhs = cls.parse_exponentiative_expr()
        if cls.at()._in(TokenType.Asterisk, TokenType.Divide, TokenType.Modulus):
            return BinaryExprNode(lhs, cls.eat().type, cls.parse_multiplicative_expr())
        return lhs
    
    @classmethod
    def parse_exponentiative_expr(cls) -> BinaryExprNode | Expr:
        lhs = cls.parse_primary_expr()
        if cls.at() == TokenType.Exponentiation:
            return BinaryExprNode(lhs, cls.eat().type, cls.parse_exponentiative_expr())
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
        ) -> IntNode | FloatNode | StrNode | BoolNode | NullNode | IdentifierNode:
        match cls.at().type:
            case TokenType.Identifier if TokenType.Identifier not in exclude:
                return IdentifierNode(cls.eat().value)
            case TokenType.Int if TokenType.Int not in exclude:
                return IntNode(cls.eat().value)
            case TokenType.Float if TokenType.Float not in exclude:
                return FloatNode(cls.eat().value)
            case TokenType.Str if TokenType.Str not in exclude:
                return StrNode(cls.eat().value)
            case TokenType.Bool if TokenType.Bool not in exclude:
                return BoolNode(cls.eat().value)
            case TokenType.Null if TokenType.Null not in exclude:
                cls.eat()
                return NullNode()
            case TokenType.OpenParenthesis if TokenType.OpenParenthesis not in exclude:
                cls.eat()
                expr = cls.parse_expr()
                cls.asrt(TokenType.CloseParenthesis)
                return expr
            case _:
                raise Exception(...) 