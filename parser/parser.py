import typing
from lexer.lexer import Token
from lexer.tokens import TokenType as TokenType
import parser.nodes as Nodes

class Parser:
    def __new__(cls) -> typing.NoReturn:
        raise Exception("This class is not supposed to be inherited.")
    
    tokens: typing.List[Token]
    
    @classmethod
    def produce_ast(cls, tokens: typing.List[Token]) -> Nodes.Program:
        cls.tokens = tokens
        program = Nodes.Program()
        while cls.at() != TokenType.EoF:
            program.body.append(cls.parse_stmts())
            if cls.at() != TokenType.EoF:
                cls.eat({TokenType.NewLine, TokenType.Semicolon})
        del cls.tokens
        return program
    
    @classmethod
    def at(cls):
        return cls.tokens[0]
    
    @classmethod
    def at_is(cls, type: typing.Union[TokenType, typing.Set[TokenType]]) -> Token:
        if not isinstance(type, set): 
            type = {type}
        return cls.at().type in type
    
    @classmethod
    def eat(cls, type: typing.Union[TokenType, typing.Set[TokenType], None] = None) -> Token:
        tkn = cls.tokens.pop(0)
        if type is not None:
            if isinstance(type, TokenType): 
                type = {type}
            
            if tkn.type not in type:
                raise ValueError("e")
        return tkn
    
    @classmethod
    def remove_new_lines(cls) -> None:
        if cls.at() == TokenType.NewLine:
            cls.eat()

    @classmethod
    def parse_stmts(cls) -> Nodes.AllStmtsTypeHint:
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
    def parse_var_declaration(cls) -> Nodes.VarDeclaration:
        constant = cls.eat() == TokenType.Const
        name = cls.eat(TokenType.Identifier).value
        if cls.at_is(TokenType.AssignOper):
            cls.eat()
            value = cls.parse_expr()
        else:
            value = None
        return Nodes.VarDeclaration(name, value, constant) # type: ignore
    
    @classmethod
    @typing.overload
    def parse_conditional(cls, clause: typing.Literal[TokenType.If, TokenType.Elif]) -> Nodes.Conditional: ...
    
    @classmethod
    @typing.overload
    def parse_conditional(cls, clause: typing.Literal[TokenType.Else]) -> Nodes.CodeBlock: ...
    
    @classmethod
    def parse_conditional(cls, clause):
        cls.eat(clause)
        
        if clause != TokenType.Else:
            cond = cls.parse_expr()
        
        code = cls.parse_attached_code_block()
        
        # ? This checks on the `else`
        # ? If it is, just return the code block
        # ? Without any attempt at continuation
        if clause == TokenType.Else:
            return code

        # ? 
        if cls.at_is({TokenType.Elif, TokenType.Else}):
            return Nodes.Conditional(cond, code, cls.parse_conditional(cls.at().type))
        return Nodes.Conditional(cond, code)
    
    @classmethod
    def parse_while_stmt(cls) -> Nodes.WhileLoop:
        cls.eat(TokenType.While)
        cond = cls.parse_expr()
        
        code = cls.parse_attached_code_block()
        
        els = None
        
        # An `else` statement
        if cls.at_is(TokenType.Else):
            cls.eat(TokenType.Else)
            els = cls.parse_attached_code_block()
        
        return Nodes.WhileLoop(cond, code, els)
    
    @classmethod
    def parse_assignment_stmt(cls) -> Nodes.AllExprTypeHint | Nodes.Assignment:
        lhs = cls.parse_expr()
        match cls.at():
            case TokenType.AssignOper:
                exprs = [lhs]
                while cls.at_is(TokenType.AssignOper):
                    cls.eat()
                    exprs.append(cls.parse_expr())
                return Nodes.Assignment(exprs)
            case TokenType.ModifierAssignOper:
                return Nodes.ModifierAssignment(lhs, cls.eat().value, cls.parse_expr())
        return lhs
    
    @classmethod
    def parse_expr(cls) -> Nodes.Expr:
        return cls.parse_assignment_expr()
    
    @classmethod
    def parse_attached_code_block(cls) -> Nodes.CodeBlock:
        # ^ Create a code block
        code = Nodes.CodeBlock()
        
        # ? If the code block uses {}
        if cls.at_is(TokenType.OpenCurlyBrace):
            cls.eat(TokenType.OpenCurlyBrace)
            
            # Idk
            while True:
                code.append(cls.parse_stmts())
                if cls.at_is(TokenType.CloseCurlyBrace):
                    break
                cls.eat({TokenType.NewLine, TokenType.Semicolon})
            cls.eat(TokenType.CloseCurlyBrace)
        else:
            # ? If the code block doesn't use {}
            code.append(cls.parse_stmts())
        
        return code
    
    @classmethod
    def parse_assignment_expr(cls) -> Nodes.AllExprTypeHint:
        lhs = cls.parse_collections_expr()
        if cls.at_is(TokenType.WalrusOper):
            return Nodes.WalrusExpr(lhs, cls.eat().value, cls.parse_collections_expr())
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
    def parse_ternary_expr(cls) -> Nodes.AllExprTypeHint:
        cond = cls.parse_logical_expr()
        if cls.at_is(TokenType.QuestionMark):
            cls.eat()
            true_expr = cls.parse_expr()
            if cls.at_is(TokenType.GDCologne):
                cls.eat()
                return Nodes.Ternary(cond, true_expr, cls.parse_expr())
            return Nodes.Ternary(cond, true_expr, Nodes.Null())
        return cond
    
    @classmethod
    def parse_logical_expr(cls) -> Nodes.AllExprTypeHint:
        lhs = cls.parse_condition_expr()
        if cls.at_is({TokenType.Caret, TokenType.Xor}):
            return Nodes.Binary(lhs, TokenType.Xor, cls.parse_logical_expr())
        if cls.at_is({TokenType.VerticalBar, TokenType.Or}):
            return Nodes.Binary(lhs, TokenType.Or, cls.parse_logical_expr())
        if cls.at_is({TokenType.Andpersand, TokenType.And}):
            return Nodes.Binary(lhs, TokenType.And, cls.parse_logical_expr())
        return lhs
    
    @classmethod
    def parse_condition_expr(cls) -> Nodes.AllExprTypeHint:
        lhs = cls.parse_additive_expr()
        if cls.at_is({TokenType.GreaterThan, TokenType.GreaterEqualThan, 
                     TokenType.Equal, TokenType.NotEqual, 
                     TokenType.LessEqualThan, TokenType.LessThan}):
            comp_tokens = []; exprs = []
            while cls.at_is({TokenType.GreaterThan, TokenType.GreaterEqualThan, 
                           TokenType.Equal, TokenType.NotEqual, 
                           TokenType.LessEqualThan, TokenType.LessThan}):
                comp_tokens.append(cls.eat().type)
                exprs.append(cls.parse_additive_expr())
            return Nodes.Comparison(lhs, comp_tokens, exprs)
        return lhs
    
    @classmethod
    def parse_additive_expr(cls) -> Nodes.AllExprTypeHint:
        lhs = cls.parse_multiplicative_expr()
        if cls.at_is({TokenType.Plus, TokenType.Minus}):
            return Nodes.Binary(lhs, cls.eat().type, cls.parse_additive_expr())
        return lhs
    
    @classmethod
    def parse_multiplicative_expr(cls) -> Nodes.AllExprTypeHint:
        lhs = cls.parse_exponentiative_expr()
        if cls.at_is({TokenType.Asterisk, TokenType.TrueDivision, 
                     TokenType.FloorDivision, TokenType.Modulus}):
            return Nodes.Binary(lhs, cls.eat().type, cls.parse_multiplicative_expr())
        return lhs
    
    @classmethod
    def parse_exponentiative_expr(cls) -> Nodes.AllExprTypeHint:
        lhs = cls.parse_unary_expr()
        if cls.at_is(TokenType.Exponentiation):
            return Nodes.Binary(lhs, cls.eat().type, cls.parse_exponentiative_expr())
        return lhs
    
    @classmethod
    def parse_unary_expr(cls) -> Nodes.AllExprTypeHint:
        """
        Parses all unary expressions. This include:
        - Prefix: `++`, `--`, `!`, `~`, `not`, `*`, `+`, `-`
        - Postfix: `++`, `--`
        """
        if cls.at_is({TokenType.Plus, TokenType.Minus, TokenType.Asterisk, 
                     TokenType.Tilda, TokenType.Not, TokenType.Exclamation, 
                     TokenType.Incre, TokenType.Decre}):
            return Nodes.Unary(attachment = cls.eat().type, expr = cls.parse_primary_expr(), position = "Prefix")
        expr = cls.parse_primary_expr()
        if cls.at_is({TokenType.Incre, TokenType.Decre}):
            return Nodes.Unary(expr, cls.eat().type, "Postfix")
        return expr
    
    @classmethod
    def parse_member_subscription_call_expr(cls) -> Nodes.AllExprTypeHint:
        """
        Parses both member access (a.b), subscription access (a[b]) and function call (a(b)) expressions.
        """
        member = cls.parse_member_subscription_expr()
        
        if cls.at_is(TokenType.OpenParenthesis):
            return cls.parse_call_expr(member)
        return member
    
    @classmethod
    def parse_member_subscription_expr(cls) -> Nodes.AllExprTypeHint: 
        obj = cls.parse_primary_expr()
        while cls.at_is({TokenType.Dot, TokenType.OpenSquareBracket}):
            propert: Nodes.Expr
            if cls.eat() == TokenType.Dot:
                node = Nodes.MemberAccess
                propert = cls.parse_primary_expr(exclude = {TokenType.Int, TokenType.Float, 
                                                        TokenType.Str, TokenType.Bool, 
                                                        TokenType.Null, TokenType.OpenParenthesis})
            else:
                node = Nodes.Subscription
                propert = cls.parse_expr()
                cls.eat(TokenType.CloseSquareBracket)
            obj = node(obj, propert)
        return obj
    
    @classmethod
    def parse_call_expr(cls, caller: Nodes.Expr) -> Nodes.Call:
        call_expr = Nodes.Call(caller, cls.parse_call_args())
        if (cls.at_is(TokenType.OpenParenthesis)):
            call_expr = cls.parse_call_expr(call_expr)
        return call_expr
    
    @classmethod
    def parse_call_args(cls) -> Nodes.CallArgumentList:
        cls.eat(TokenType.OpenParenthesis)
        args = Nodes.CallArgumentList() if cls.at() == TokenType.CloseParenthesis else cls.parse_positional_call_args()
        cls.expect(TokenType.CloseParenthesis)
        return args
    
    @classmethod
    def parse_positional_call_args(cls) -> Nodes.CallArgumentList:
        positional_args = [cls.parse_expr()]

        while cls.at_is(TokenType.Comma):
            cls.eat()
            arg = cls.parse_expr()
            if isinstance(arg, Nodes.Identifier) and cls.at_is(TokenType.AssignOper):
                arg: Nodes.Identifier
                return Nodes.CallArgumentList(positional_args, cls.parse_keyword_call_args(arg.symbol))
            positional_args.push(arg)

        return Nodes.CallArgumentList(positional_args)
    
    @classmethod
    def parse_keyword_call_args(cls, initial_ident_name: str) -> typing.Dict[str, Nodes.Expr]:
        keyword_args: typing.Dict[str, Nodes.Expr] = {}
        cls.eat(TokenType.AssignOper)
        keyword_args.setdefault(initial_ident_name, cls.parse_expr())
        if cls.at_is(TokenType.Comma):
            while cls.at_is(TokenType.Comma):
                key = cls.parse_primary_expr({TokenType.Int, TokenType.Float, TokenType.Str, 
                                              TokenType.Bool, TokenType.Null, TokenType.OpenParenthesis})
                cls.eat(TokenType.AssignOper)
                keyword_args.setdefault(key.symbol, cls.parse_expr())
        elif not cls.at_is(TokenType.CloseParenthesis):
            raise Exception()
        return keyword_args
    
    @classmethod
    def parse_primary_expr(cls, exclude: typing.Set [
            typing.Literal [
                TokenType.Identifier,
                TokenType.Int,
                TokenType.Float,
                TokenType.Str,
                TokenType.Bool,
                TokenType.Null,
                TokenType.OpenParenthesis
            ]
        ] = {}) -> Nodes.Expr:
        match cls.at().type:
            case TokenType.Identifier if TokenType.Identifier not in exclude:
                return Nodes.Identifier(cls.eat().value)
            case TokenType.Int if TokenType.Int not in exclude:
                return Nodes.Int(int(cls.eat().value))
            case TokenType.Float if TokenType.Float not in exclude:
                return Nodes.Float(float(cls.eat().value))
            case TokenType.Str if TokenType.Str not in exclude:
                return Nodes.Str(cls.eat().value)
            case TokenType.Bool if TokenType.Bool not in exclude:
                return Nodes.Bool(True if cls.eat().value == "true" else False)
            case TokenType.Null if TokenType.Null not in exclude:
                cls.eat()
                return Nodes.Null()
            case TokenType.OpenParenthesis if TokenType.OpenParenthesis not in exclude:
                cls.eat()
                cls.remove_new_lines()
                expr = cls.parse_expr()
                cls.remove_new_lines()
                cls.eat(TokenType.CloseParenthesis)
                return expr
            case _:
                raise Exception(cls.tokens)