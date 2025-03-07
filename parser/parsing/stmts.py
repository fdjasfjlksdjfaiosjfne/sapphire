import sys; sys.dont_write_bytecode = True
from typing import *
from lexer.tokens import TokenType, Token
from ..ast import *

def parse_stmt(self: Self) -> Stmt:
    self.remove_trailing_new_lines()
    match self.at().type:
        case TokenType.Decorator:
            decorators: Set[Token] = {self.eat()}
            while self.at().type == TokenType.Decorator:
                decorators.add(self.eat().value[1:])
            match self.at().type:
                case TokenType.Fn:
                    return self.parse_fn_declaration(decorators)
                case TokenType.Class:
                    return self.parse_class_declaration(decorators)
                case _:
                    raise Exception("placeholder")
        case TokenType.Fn:
            return self.parse_fn_declaration()
        case TokenType.Class:
            return self.parse_class_declaration()
        case TokenType.Let | TokenType.Const:
            return self.parse_var_decalration()
        case _:
            return self.parse_assignment()

def parse_var_declaration(self: Self):
    is_constant = self.eat().type == TokenType.Const
    name = self.assrt(TokenType.Identifier, "placeholder")
    # Type hints
    if self.at().type == TokenType.GDCologne:
        self.eat()
        type_hint = self.parse_type_hints()

@overload
def parse_fn_declaration(self: Self) -> FunctionDeclaration: ...

@overload
def parse_fn_declaration(self: Self, decorators: Set[]) -> FunctionDeclaration: ...

def parse_fn_declaration(self: Self) -> FunctionDeclaration:
    self.eat() # Eat the fn
    
    return FunctionDeclaration()

def parse_assignment(self: Self, *, force_expr: bool = False) -> VarAssignmentStmt | VarAssignmentExpr | Expr:
    self.remove_trailing_new_lines()
    left = self.parse_collections_expr()
    if self.at().type == TokenType.AssignOper:
        if assign_oper := self.eat().value in {"c:=", ":=", "i:="}:
            return VarAssignmentExpr(left, assign_oper, self.parse_assignment(force_expr = force_expr))
        if force_expr:
            raise Exception("placeholder")
        return VarAssignmentStmt(left, assign_oper, self.parse_assignment(force_expr = force_expr))
    return left