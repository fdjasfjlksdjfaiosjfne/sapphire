import sys; sys.dont_write_bytecode = True
from typing import *
from lexer.tokens import TokenType, Token
from ..ast import *

# TODO
#^ Orders Of Precedence:
# @ PARENTHESES ()
# * PrimaryExpr
## Call()
## Subscription[], member.access
## Unary Operators (!, not, ~, -, +, ++, --)
## "**"
## "*" / "/" / "%"
## "+" / "-"
## "|>"
## "<" / ">" / ">=" / "<=" / "==" / "!="
## "<<" / ">>"
## "b&"
## "b^"
## "b|"
## "&" and
## "|" or
## "^" xor
## Ternary Operator (a ? b : c)
## [1, 2, 3, 4] {1, 2, 3, 4} {"a": "b"} {a: "b"}
## Assignment Operator (:=)

def parse_type_hints(self: Self):
    pass

def parse_collections_expr(self: Self) -> ArrayLiteral | SetLiteral | MapLiteral | ObjLiteral | Expr:
    self.remove_trailing_new_lines()
    match self.at().type:
        # ? Objects, maps, sets
        case TokenType.OpenCurlyBrace:
            # ? Check whether it is a set
            # % TokenType.CloseCurlyBrace covers {1}
            # % TokenType.Comma covers {1,} or {1, 2, ...}
            # % TokenType.EoF covers {1 <EoF>
            if self.tokens[2] in {TokenType.CloseCurlyBrace, TokenType.Comma, TokenType.EoF}:
                return self.parse_lists()
            return self.parse_map_or_obj_expr()
        # ? Arrays
        case TokenType.OpenSquareBracket:
            return self.parse_lists()
        case _:
            return self.parse_ternary_expr()

def parse_lists(self: Self) -> ArrayLiteral | SetLiteral:
    match self.at.type:
        case TokenType.OpenCurlyBrace: 
            end_token = TokenType.CloseCurlyBrace
            add_expr = set.add
            props = set()
            NodeClass = SetLiteral
        case TokenType.OpenSquareBracket: 
            end_token = TokenType.CloseSquareBracket
            props = []
            add_expr = list.append
            NodeClass = ArrayLiteral
        case _:
            raise Exception("placeholder")
    self.eat()
    while self.at.type not in {end_token, TokenType.EoF}:
        add_expr(props, self.parse_assignment(force_expr = True))
        self.assrt(TokenType.Comma, "placeholder")
    self.assrt(end_token, "placeholder")
    return NodeClass(props)

def parse_map_or_obj_expr(self: Self) -> MapLiteral | ObjLiteral:
    self.eat() ## Eat the {
    props = {}
    if self.at.type == TokenType.Identifier:
        NodeExpr = ObjLiteral
    else:
        NodeExpr = MapLiteral
    # ? Loop until end of file or object, appending key-value pairs in the way
    while self.at not in {TokenType.CloseCurlyBrace, TokenType.EoF}:
        # ? Consume the key
        if NodeExpr == ObjLiteral:
            key = self.assrt(
                {TokenType.Identifier},
                "Expecting an identifier as a key in an object."
            ).value
        else:
            # ? This will only parse the primitives 
            # & (int, float, str, bool, null)
            key = self.parse_primary_expr(primitives_only = True)
        self.assrt(
            TokenType.GDCologne,
            "placeholder"
        )
        value = self.parse_assignment(force_expr = True)
        props.setdefault(key, value)
    return NodeExpr([Property(key, value) for key, value in props.items()])

def parse_ternary_expr(self: Self) -> TernaryExpr | Expr:
    left = self.parse_logical_expr()
    if self.at().type == TokenType.QuestionMark:
        self.eat()
        true_expr = self.parse_logical_expr()
        self.assrt(TokenType.GDCologne, "placeholder")
        false_expr = self.parse_logical_expr()
        left = TernaryExpr(left, true_expr, false_expr)
    return left

def parse_logical_expr(self) -> BinaryExpr | Expr:
    left = self.parse_binary_expr()
    if self.at().type == TokenType.LogicalOper:
        oper = self.eat().value
        right = self.parse_binary_expr()
        left = BinaryExpr(left, oper, right)
    return left

## b^ b| b&
def parse_binary_expr(self) -> BinaryExpr | Expr:
    left = self.parse_condition_expr()
    if self.at().type == TokenType.BinaryOper:
        oper = self.eat().value
        right = self.parse_condition_expr()
        left = BinaryExpr(left, oper, right)
    return left

def parse_condition_expr(self) -> BinaryExpr | Expr:
    left = self.parse_additive_expr()
    if self.at().type == TokenType.CompOper:
        oper = self.eat().value
        right = self.parse_additive_expr()
        left = BinaryExpr(left, oper, right)
    return left

def parse_additive_expr(self) -> BinaryExpr | Expr:
    left = self.parse_multiplicative_expr()
    if self.at().type in {TokenType.Plus, TokenType.Minus}:
        oper = self.eat().value
        right = self.parse_multiplicative_expr()
        left = BinaryExpr(left, oper, right)
    return left

def parse_multiplicative_expr(self) -> BinaryExpr | Expr:
    left = self.parse_exponentiative_expr()
    if self.at().type in {TokenType.Asterisk, TokenType.Divide, TokenType.Modulus}:
        oper = self.eat().value
        right = self.parse_exponentiative_expr()
        left = BinaryExpr(left, oper, right)
    return left

def parse_exponentiative_expr(self) -> BinaryExpr | Expr:
    left = self.parse_unary_expr()
    if self.at().type == TokenType.Exponentiation:
        oper = self.eat().value
        right = self.parse_unary_expr()
        left = BinaryExpr(left, oper, right)
    return left

def parse_unary_expr(self) -> UnaryExpr | Expr:
    if self.at().type in {TokenType.Tilda, TokenType.Minus, TokenType.Plus, TokenType.Exclamation, TokenType.Not}:
        return UnaryExpr(symbol = self.eat(), expr = self.eat())
    expr = self.parse_member_expr()
    if self.at().type in {TokenType.Incre, TokenType.Decre}:
        return UnaryExpr(expr, self.eat().value)
    return expr

def parse_call_member_expr(self) -> CallExpr | MemberExpr | Expr:
    member = self.parse_member_expr()
    if self.at().type == TokenType.OpenParenthesis:
        self.parse_call_expr(member)
    return member

def parse_call_expr(self, caller: Expr) -> CallExpr | Expr:
    call_expr = CallExpr(caller, self.parse_args())
    if self.at().type == TokenType.OpenParenthesis:
        call_expr = self.parse_call_expr(call_expr)
    return call_expr

def parse_call_args(self) -> List[CallArgument]:
    self.assrt(TokenType.OpenParenthesis, "placeholder")
    args = [] if self.at().type == TokenType.CloseParenthesis else self.parse_arguments_list()
    self.assrt(TokenType.CloseParenthesis, "placeholder")
    return args

def parse_arguments_list(self) -> List[CallArgument]:
    args: List[CallArgument] = [self.parse_argument()]
    while self.at().type == TokenType.Comma and self.eat():
        args.append(self.parse_argument)
    return args

def parse_argument(self) -> CallArgument:
    a = self.parse_assignment(force_expr = True)
    ## Keyword arguments
    if (a.kind == NodeType.Identifier and 
        self.at().type == TokenType.AssignOper and 
        self.at().value == "="):
        self.eat()
        b = self.parse_assignment(force_expr = True)
        return CallArgument(name = a, value = b)
    return CallArgument(value = a)

def parse_member_expr(self):
    obj = self.parse_primary_expr()
    while self.at().type in {TokenType.Dot, TokenType.OpenSquareBracket}:
        operator = self.eat()
        property: Expr
        computed: bool
        
        if operator.type == TokenType.Dot:
            computed = False
            property = Identifier(self.assrt(TokenType.Identifier, "placeholrd").value)
        else:
            computed = True
            property = self.parse_assignment(force_expr = True)
            self.assrt(TokenType.CloseSquareBracket, "placehler")
        return MemberExpr(obj, property, computed)

def parse_primary_expr(self, *, primitives_only: bool = False) -> Identifier | IntLiteral | FloatLiteral | StrLiteral | BoolLiteral | NullLiteral | Expr:
    """Parse primary expressions including literals, identifiers, and grouped expressions.

    Args:
        primitives_only (bool): If True, restricts parsing to primitive types only.

    Returns:
        Parsed expression object.
    """
    match self.at().type:
        case TokenType.Identifier if not primitives_only:
            return Identifier(self.eat().value)
        case TokenType.Int:
            return IntLiteral(self.eat().value)
        case TokenType.Float:
            return FloatLiteral(self.eat().value)
        case TokenType.Str:
            return StrLiteral(self.eat().value)
        case TokenType.Bool:
            return BoolLiteral(self.eat().value)
        case TokenType.Null:
            self.eat()
            return NullLiteral()
        case TokenType.OpenParenthesis if not primitives_only:
            self.eat()
            self.remove_trailing_new_lines()
            value = self.parse_assignment(force_expr = True)
            self.assrt(
                TokenType.CloseParenthesis,
                "placeholder",
                remove_trailing_new_line = True
            )
            return value
        case _:
            raise Exception("placeholdr")