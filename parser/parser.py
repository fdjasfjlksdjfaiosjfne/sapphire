from typing import List, Set, Literal, Union, TypeVar, Generic, overload
from lexer.lexer import Token
from lexer.tokens import TokenType as TT
from enum import Enum
import parser.nodes as N

class Matches(Enum):
    def __rmatmul__(self, value):
        """
        # This is NOT used to matrix multiplication. Please don't get mistaken. Thank you.
        """
        if isinstance(value, Token):
            value = value.type
        elif not isinstance(value, TT): 
            value = value.at()
        return value in self
    
    def __contains__(self, value):
        return value.type in self.value
    
    Additive = {TT.Plus, TT.Minus}
    Multiplicative = {TT.Asterisk, TT.Divide, TT.Modulus}
    Comparative = {TT.GreaterThan, TT.GreaterEqualThan, TT.Equal, TT.NotEqual, TT.LessEqualThan, TT.LessThan}
    Xor = {TT.Caret, TT.Xor}
    Or = {TT.VerticalBar, TT.Or}
    And = {TT.Andpersand, TT.And}
    ConditionalContinuation = {TT.Elif, TT.Else}
    AssignOpers = {TT.AssignOper, TT.ModifierAssignOper}
    temp = None

T = TypeVar("T")

class Maybe(Generic[T]):
    def __class_getitem__(cls, hint: T) -> Union[T, int]:
        return Union[hint, N.Expr]

class Parser:
    
    class Hints(Enum): 
        ParsePrimaryExprExclusion = Set [
            Literal [
                TT.Identifier,
                TT.Int,
                TT.Float,
                TT.Str,
                TT.Bool,
                TT.Null,
                TT.OpenParenthesis
            ]
        ]
        
        ParsePrimaryExprReturn = Maybe [
            Union [
                N.IntNode,
                N.FloatNode,
                N.StrNode,
                N.BoolNode,
                N.NullNode,
                N.IdentifierNode,
            ]
        ]
        
        ConditionalClause = Literal[TT.If, TT.Elif, TT.Else]
    
    @classmethod
    def produce_ast(cls, tokens: List[Token]) -> N.ProgramNode:
        cls.tokens = tokens
        program = N.ProgramNode([])
        while cls.at() != TT.EoF:
            cls.remove_new_lines()
            program.body.append(cls.parse_stmt_and_keywords())
        del cls.tokens
        return program

    @classmethod
    def at(cls) -> Token:
        return cls.tokens[0]

    @classmethod
    def eat(cls) -> Token:
        return cls.tokens.pop(0)
    
    @classmethod
    def asrt(cls, type: TT | Set[TT] | Matches) -> Token:
        if not isinstance(type, set): 
            type = {type}
        
        if (tkn := cls.eat()).type not in type:
            raise ValueError("e")
        return tkn
    
    @classmethod
    def remove_new_lines(cls) -> None:
        if cls.at() == TT.NewLine:
            cls.eat()

    @classmethod
    def parse_stmt_and_keywords(cls) -> Maybe[N.Stmt]:
        match cls.at():
            case TT.If:
                return cls.parse_conditional(TT.If)
            case TT.While:
                return cls.parse_while_stmt()
            case _:
                return cls.parse_assignment_stmt()
    
    @overload
    def parse_conditional(cls, clause: Literal[TT.If, TT.Elif]) -> N.ConditionalNode: ...
    
    @overload
    def parse_conditional(cls, clause: Literal[TT.Else]) -> N.CodeBlockNode: ...
    
    @classmethod
    def parse_conditional(cls, clause: Hints.ConditionalClause) -> N.ConditionalNode | N.CodeBlockNode:
        cls.asrt(clause)
        if clause != TT.Else:
            cond = cls.parse_expr()
        cls.asrt(TT.OpenCurlyBrace)
        code = N.CodeBlockNode()
        while cls.at() != TT.CloseCurlyBrace:
            code.append(cls.parse_stmt_and_keywords())
        
        cls.asrt(TT.CloseCurlyBrace)
        
        if clause == TT.Else:
            return code

        if cls @ Matches.ConditionalContinuation:
            return N.ConditionalNode(cond, code, cls.parse_conditional(cls.at().type))
        return N.ConditionalNode(cond, code)
    
    @classmethod
    def parse_assignment_stmt(cls) -> Maybe[N.AssignmentNode]:
        lhs = cls.parse_expr()
        if cls @ Matches.AssignOpers:
            return N.AssignmentNode(lhs, cls.eat().value, cls.parse_assignment_expr())
        return lhs
    
    @classmethod
    def parse_expr(cls) -> N.Expr:
        return cls.parse_assignment_expr()
    
    @classmethod
    def parse_assignment_expr(cls) -> Maybe[N.WalrusExprNode]:
        lhs = cls.parse_collections_expr()
        if cls.at() == TT.WalrusOper:
            return N.WalrusExprNode(lhs, cls.eat().value, cls.parse_collections_expr())
        return lhs
    
    @classmethod
    def parse_collections_expr(cls):
        match cls.at():
            case TT.OpenCurlyBrace:
                cls.eat()
                raise Exception()
            case TT.OpenSquareBracket:
                cls.eat()
                raise Exception()
            case _:
                return cls.parse_ternary_expr()
    
    @classmethod
    def parse_ternary_expr(cls) -> Maybe[N.TernaryNode]:
        cond = cls.parse_logical_expr()
        if cls.at() == TT.QuestionMark:
            cls.eat()
            true_expr = cls.parse_expr()
            if cls.at() == TT.GDCologne:
                cls.eat()
                return N.TernaryNode(cond, true_expr, cls.parse_expr())
            return N.TernaryNode(cond, true_expr, N.NullNode())
        return cond
    
    @classmethod
    def parse_logical_expr(cls) -> Maybe[N.BinaryExprNode]:
        lhs = cls.parse_condition_expr()
        if cls @ Matches.Xor:
            return N.BinaryExprNode(lhs, TT.Xor, cls.parse_logical_expr())
        if cls @ Matches.Or:
            return N.BinaryExprNode(lhs, TT.Or, cls.parse_logical_expr())
        if cls @ Matches.And:
            return N.BinaryExprNode(lhs, TT.And, cls.parse_logical_expr())
        return lhs
    
    @classmethod
    def parse_condition_expr(cls) -> Maybe[N.ComparisonNode]:
        lhs = cls.parse_additive_expr()
        if cls @ Matches.Comparative:
            comp_tokens = []; exprs = []
            while cls @ cls.matching_sets["comparitive"]:
                comp_tokens.append(cls.eat().type)
                exprs.append(cls.parse_additive_expr())
            return N.ComparisonNode(lhs, comp_tokens, exprs)
        return lhs
    
    @classmethod
    def parse_additive_expr(cls) -> Maybe[N.BinaryExprNode]:
        lhs = cls.parse_multiplicative_expr()
        if cls @ Matches.Additive:
            return N.Binarynd.ExprNode(lhs, cls.eat().type, cls.parse_additive_expr())
        return lhs
    
    @classmethod
    def parse_multiplicative_expr(cls) -> Maybe[N.BinaryExprNode]:
        lhs = cls.parse_exponentiative_expr()
        if cls @ Matches.Multiplicative:
            return N.Binarynd.ExprNode(lhs, cls.eat().type, cls.parse_multiplicative_expr())
        return lhs
    
    @classmethod
    def parse_exponentiative_expr(cls) -> Maybe[N.BinaryExprNode]:
        lhs = cls.parse_primary_expr()
        if cls.at() == TT.Exponentiation:
            return N.Binarynd.ExprNode(lhs, cls.eat().type, cls.parse_exponentiative_expr())
        return lhs
    
    @classmethod
    def parse_primary_expr(cls, exclude: Hints.ParsePrimaryExprExclusion = {}) -> Hints.ParsePrimaryExprReturn:
        match cls.at().type:
            case TT.Identifier if TT.Identifier not in exclude:
                return N.IdentifierNode(cls.eat().value)
            case TT.Int if TT.Int not in exclude:
                return N.IntNode(int(cls.eat().value))
            case TT.Float if TT.Float not in exclude:
                return N.FloatNode(float(cls.eat().value))
            case TT.Str if TT.Str not in exclude:
                return N.StrNode(cls.eat().value)
            case TT.Bool if TT.Bool not in exclude:
                return N.BoolNode(True if cls.eat().value == "true" else False)
            case TT.Null if TT.Null not in exclude:
                cls.eat()
                return N.NullNode()
            case TT.OpenParenthesis if TT.OpenParenthesis not in exclude:
                cls.eat()
                cls.remove_new_lines()
                expr = cls.parse_expr()
                cls.remove_new_lines()
                cls.asrt(TT.CloseParenthesis)
                return expr
            case _:
                raise Exception(cls.tokens)