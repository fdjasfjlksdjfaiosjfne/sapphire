from typing import List, Set, Literal, Union, overload, NoReturn, Dict
from lexer.lexer import Token
from lexer.tokens import TokenType as TokenType
from enum import Enum
import parser.nodes as Node
from parser.nodes import NodeType

class Matches(Enum):
    def __rmatmul__(self, value):
        """
        # This is NOT used to matrix multiplication. Please don't get mistaken. Thank you.
        """
        if isinstance(value, Token):
            value = value.type
        elif not isinstance(value, TokenType): 
            value = value.at()
        return value in self
    
    def __contains__(self, value):
        return (value if isinstance(value, TokenType) else value.type) in self.value
    
    Additive = {TokenType.Plus, TokenType.Minus}
    Multiplicative = {TokenType.Asterisk, TokenType.TrueDivision, TokenType.FloorDivision, TokenType.Modulus}
    Comparative = {TokenType.GreaterThan, TokenType.GreaterEqualThan, TokenType.Equal, TokenType.NotEqual, TokenType.LessEqualThan, TokenType.LessThan}
    Xor = {TokenType.Caret, TokenType.Xor}
    Or = {TokenType.VerticalBar, TokenType.Or}
    And = {TokenType.Andpersand, TokenType.And}
    ConditionalContinuation = {TokenType.Elif, TokenType.Else}
    SinisterUnarys = {TokenType.Plus, TokenType.Minus, TokenType.Asterisk, TokenType.Tilda, TokenType.Not, TokenType.Exclamation, TokenType.Incre, TokenType.Decre}
    DexterUnarys = {TokenType.Incre, TokenType.Decre}
    StatementTerminator = {TokenType.NewLine, TokenType.Semicolon}
    StartOfAttrAccess = {TokenType.Dot, TokenType.OpenSquareBracket}
    PrimaryExprs = {TokenType.Int, TokenType.Float, TokenType.Str, TokenType.Bool, TokenType.Null, TokenType.Identifier, TokenType.OpenParenthesis}

class Parser:
    def __new__(self) -> NoReturn:
        raise Exception("This class is not supposed to be inherited.")
    
    tokens: List[Token]
    class Hints(Enum): 
        ParsePrimaryExprExclusion = Set [
            Literal [
                TokenType.Identifier,
                TokenType.Int,
                TokenType.Float,
                TokenType.Str,
                TokenType.Bool,
                TokenType.Null,
                TokenType.OpenParenthesis
            ]
        ]
        
        ConditionalClause = Literal[TokenType.If, TokenType.Elif, TokenType.Else]
    
    @classmethod
    def produce_ast(cls, tokens: List[Token]) -> Node.Program:
        cls.tokens = tokens
        program = Node.Program()
        while cls.at() != TokenType.EoF:
            program.body.append(cls.parse_stmt_and_keywords())
            cls.eat(Matches.StatementTerminator)
        del cls.tokens
        return program

    @classmethod
    def at(cls) -> Token:
        return cls.tokens[0]
    
    @classmethod
    def eat(cls, type: TokenType | Set[TokenType] | Matches | None = None) -> Token:
        tkn = cls.tokens.pop(0)
        if type is not None:
            if not isinstance(type, (set, Matches)): 
                type = {type}
            
            if tkn.type not in type:
                raise ValueError("e")
        return tkn
    
    @classmethod
    def remove_new_lines(cls) -> None:
        if cls.at() == TokenType.NewLine:
            cls.eat()

    @classmethod
    def parse_stmt_and_keywords(cls) -> Node.AllStmtsTypeHint:
        match cls.at():
            case TokenType.Let | TokenType.Const:
                return cls.parse_var_declaration()
            case TokenType.If:
                return cls.parse_conditional(TokenType.If)
            case TokenType.While:
                return cls.parse_while_stmt()
            case _:
                return cls.parse_assignment_stmt()
    
    @classmethod
    def parse_var_declaration(cls) -> Node.VarDeclaration:
        constant = cls.eat() == TokenType.Const
        name = cls.eat(TokenType.Identifier).value
        if cls.at() == TokenType.AssignOper:
            cls.eat()
            value = cls.parse_expr()
        else:
            value = None
        return Node.VarDeclaration(name, value, constant)
    
    @overload
    def parse_conditional(cls, clause: Literal[TokenType.If, TokenType.Elif]) -> Node.Conditional: ...
    
    @overload
    def parse_conditional(cls, clause: Literal[TokenType.Else]) -> Node.CodeBlock: ...
    
    @classmethod
    def parse_conditional(cls, clause: Hints.ConditionalClause) -> Node.Conditional | Node.CodeBlock:
        cls.eat(clause)
        if clause != TokenType.Else:
            cond = cls.parse_expr()
        cls.eat(TokenType.OpenCurlyBrace)
        code = Node.CodeBlock()
        while cls.at() != TokenType.CloseCurlyBrace:
            code.append(cls.parse_stmt_and_keywords())
            cls.eat(Matches.StatementTerminator)
        
        cls.eat(TokenType.CloseCurlyBrace)
        
        if clause == TokenType.Else:
            return code

        if cls @ Matches.ConditionalContinuation:
            return Node.Conditional(cond, code, cls.parse_conditional(cls.at().type))
        return Node.Conditional(cond, code)
    
    @classmethod
    def parse_assignment_stmt(cls) -> Node.AllExprTypeHint | Node.Assignment:
        lhs = cls.parse_expr()
        match cls.at():
            case TokenType.AssignOper:
                exprs = [lhs]
                while cls.at() == TokenType.AssignOper:
                    cls.eat()
                    exprs.append(cls.parse_expr())
                return Node.Assignment(exprs)
            case TokenType.ModifierAssignOper:
                return Node.ModifierAssignment(lhs, cls.eat().value, cls.parse_expr())
        return lhs
    
    @classmethod
    def parse_expr(cls) -> Node.Expr:
        return cls.parse_assignment_expr()
    
    @classmethod
    def parse_assignment_expr(cls) -> Node.AllExprTypeHint:
        lhs = cls.parse_collections_expr()
        if cls.at() == TokenType.WalrusOper:
            return Node.WalrusExpr(lhs, cls.eat().value, cls.parse_collections_expr())
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
    def parse_ternary_expr(cls) -> Node.AllExprTypeHint:
        cond = cls.parse_logical_expr()
        if cls.at() == TokenType.QuestionMark:
            cls.eat()
            true_expr = cls.parse_expr()
            if cls.at() == TokenType.GDCologne:
                cls.eat()
                return Node.Ternary(cond, true_expr, cls.parse_expr())
            return Node.Ternary(cond, true_expr, Node.Null())
        return cond
    
    @classmethod
    def parse_logical_expr(cls) -> Node.AllExprTypeHint:
        lhs = cls.parse_condition_expr()
        if cls @ Matches.Xor:
            return Node.Binary(lhs, TokenType.Xor, cls.parse_logical_expr())
        if cls @ Matches.Or:
            return Node.Binary(lhs, TokenType.Or, cls.parse_logical_expr())
        if cls @ Matches.And:
            return Node.Binary(lhs, TokenType.And, cls.parse_logical_expr())
        return lhs
    
    @classmethod
    def parse_condition_expr(cls) -> Node.AllExprTypeHint:
        lhs = cls.parse_additive_expr()
        if cls @ Matches.Comparative:
            comp_tokens = []; exprs = []
            while cls @ cls.matching_sets["comparitive"]:
                comp_tokens.append(cls.eat().type)
                exprs.append(cls.parse_additive_expr())
            return Node.Comparison(lhs, comp_tokens, exprs)
        return lhs
    
    @classmethod
    def parse_additive_expr(cls) -> Node.AllExprTypeHint:
        lhs = cls.parse_multiplicative_expr()
        if cls @ Matches.Additive:
            return Node.Binarynd.Expr(lhs, cls.eat().type, cls.parse_additive_expr())
        return lhs
    
    @classmethod
    def parse_multiplicative_expr(cls) -> Node.AllExprTypeHint:
        lhs = cls.parse_exponentiative_expr()
        if cls @ Matches.Multiplicative:
            return Node.Binarynd.Expr(lhs, cls.eat().type, cls.parse_multiplicative_expr())
        return lhs
    
    @classmethod
    def parse_exponentiative_expr(cls) -> Node.AllExprTypeHint:
        lhs = cls.parse_unary_expr()
        if cls.at() == TokenType.Exponentiation:
            return Node.Binarynd.Expr(lhs, cls.eat().type, cls.parse_exponentiative_expr())
        return lhs
    
    @classmethod
    def parse_unary_expr(cls) -> Node.AllExprTypeHint:
        """
        Parses all unary expressions. This include:
        - Prefix: `++`, `--`, `!`, `~`, `not`, `*`, `+`, `-`
        - Postfix: `++`, `--`
        """
        if cls.at() @ Matches.SinisterUnarys:
            return Node.Unary(attachment = cls.eat().type, expr = cls.parse_primary_expr(), position = "Prefix")
        expr = cls.parse_primary_expr()
        if cls.at() @ Matches.DexterUnarys:
            return Node.Unary(expr, cls.eat().type, "Postfix")
        return expr
    
    @classmethod
    def parse_member_subscription_call_expr(cls) -> Node.AllExprTypeHint:
        """
        Parses both member access (a.b), subscription access (a[b]) and function call (a(b)) expressions.
        """
        member = cls.parse_member_subscription_expr()
        
        if cls.at() == TokenType.OpenParenthesis:
            return cls.parse_call_expr(member)
        return member
    
    @classmethod
    def parse_member_subscription_expr(cls) -> Node.AllExprTypeHint: 
        obj = cls.parse_primary_expr()
        while cls.at() == Matches.StartOfAttrAccess:
            propert: Node.Expr
            if cls.eat() == TokenType.Dot:
                node = Node.MemberAccess
                propert = cls.parse_primary_expr(exclude = Matches.PrimaryExprs.value - {TokenType.Identifier})
            else:
                node = Node.Subscription
                propert = cls.parse_expr()
                cls.eat(TokenType.CloseSquareBracket)
            obj = node.__init__(obj, propert)
        return obj
    
    @classmethod
    def parse_call_expr(cls, caller: Node.Expr) -> Node.Call:
        call_expr = Node.Call(caller, cls.parse_call_args())
        if (cls.at().type == TokenType.OpenParenthesis):
            call_expr = cls.parse_call_expr(call_expr)
        return call_expr
    
    @classmethod
    def parse_call_args(cls) -> Node.CallArgumentList:
        cls.eat(TokenType.OpenParenthesis)
        args = Node.CallArgumentList() if cls.at() == TokenType.CloseParenthesis else cls.parse_positional_call_args()
        cls.expect(TokenType.CloseParenthesis)
        return args
    
    @classmethod
    def parse_positional_call_args(cls) -> Node.CallArgumentList:
        positional_args = [cls.parse_expr()]

        while cls.at() == TokenType.Comma:
            cls.eat()
            arg = cls.parse_expr()
            if arg == NodeType.Identifier and cls.at() == TokenType.AssignOper:
                arg: Node.Identifier
                return Node.CallArgumentList(positional_args, cls.parse_keyword_call_args(arg.symbol))
            positional_args.push(arg)

        return Node.CallArgumentList(positional_args)
    
    @classmethod
    def parse_keyword_call_args(cls, initial_ident_name: str) -> Dict[str, Node.Expr]:
        keyword_args: Dict[str, Node.Expr] = {}
        cls.eat(TokenType.AssignOper)
        keyword_args.setdefault(initial_ident_name, cls.parse_expr())
        if cls.at() == TokenType.Comma:
            while cls.at() == TokenType.Comma:
                key = cls.parse_primary_expr(Matches.PrimaryExprs - {TokenType.Identifier})
                cls.eat(TokenType.AssignOper)
                keyword_args.setdefault(key.symbol, cls.parse_expr())
        elif cls.at() != TokenType.CloseParenthesis:
            raise Exception()
        return keyword_args
    
    @classmethod
    def parse_primary_expr(cls, exclude: Hints.ParsePrimaryExprExclusion = {}) -> Hints.ParsePrimaryExprReturn:
        match cls.at().type:
            case TokenType.Identifier if TokenType.Identifier not in exclude:
                return Node.Identifier(cls.eat().value)
            case TokenType.Int if TokenType.Int not in exclude:
                return Node.Int(int(cls.eat().value))
            case TokenType.Float if TokenType.Float not in exclude:
                return Node.Float(float(cls.eat().value))
            case TokenType.Str if TokenType.Str not in exclude:
                return Node.Str(cls.eat().value)
            case TokenType.Bool if TokenType.Bool not in exclude:
                return Node.Bool(True if cls.eat().value == "true" else False)
            case TokenType.Null if TokenType.Null not in exclude:
                cls.eat()
                return Node.Null()
            case TokenType.OpenParenthesis if TokenType.OpenParenthesis not in exclude:
                cls.eat()
                cls.remove_new_lines()
                expr = cls.parse_expr()
                cls.remove_new_lines()
                cls.eat(TokenType.CloseParenthesis)
                return expr
            case _:
                raise Exception(cls.tokens)