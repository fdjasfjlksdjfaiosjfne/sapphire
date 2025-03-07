import sys; sys.dont_write_bytecode = True
from typing import *
from lexer.tokens import TokenType, Token
from .ast import *
from parsing import stmts, exprs

class Parser:
    def __init__(self):
        self.parse_stmt = stmts.parse_stmt
        self.parse_fn_declaration = stmts.parse_fn_declaration
        self.parse_var_declaration = stmts.parse_var_declaration
        self.parse_assignment = stmts.parse_assignment
        # ^ EXPR
        self.parse_collections_expr = exprs.parse_collections_expr
        self.parse_type_hints = exprs.parse_type_hints
        self.parse_call_expr = exprs.parse_call_expr
        self.parse_call_member_expr = exprs.parse_call_member_expr
        self.parse_lists = exprs.parse_lists
        self.parse_condition_expr = exprs.parse_condition_expr
        self.parse_binary_expr = exprs.parse_binary_expr
        self.parse_exponentiaitive_expr = exprs.parse_exponentiative_expr
        self.parse_multiplicative_expr = exprs.parse_multiplicative_expr
        self.parse_additive_expr = exprs.parse_additive_expr
        self.parse_call_args = exprs.parse_call_args
        self.parse_argument = exprs.parse_argument
        self.parse_arguments_list = exprs.parse_arguments_list
        self.parse_primary_expr = exprs.parse_primary_expr
        self.parse_map_or_obj_expr = exprs.parse_map_or_obj_expr
        self.parse_ternary_expr = exprs.parse_ternary_expr
        self.parse_logical_expr = exprs.parse_logical_expr
        self.parse_unary_expr = exprs.parse_unary_expr
        self.parse_member_expr = exprs.parse_member_expr

    def produce_ast(self, tokens: List[Token]) -> Program:
        self.tokens = tokens
        program = Program()
        while self.at().type != TokenType.EoF:
            program.body.append(self.parse_stmt())
        return program
    
    @overload
    def assrt(self, token_types: Set[TokenType], err: str, remove_trailing_new_line: bool = False) -> Token: ...
    
    @overload
    def assrt(self, token_types: TokenType, err: str, remove_trailing_new_line: bool = False) -> Token: ...
    
    def assrt(self, token_types: TokenType | Set[TokenType], err: str, remove_trailing_new_line: bool = False) -> Token:
        if isinstance(token_types, TokenType):
            token_types = {TokenType}
        if remove_trailing_new_line:
            token_types.add(TokenType.NewLine)
        if t := self.eat().type not in token_types:
            raise Exception(str)
        return t
    
    def at(self, remove_trailing_new_line: bool = False) -> Token:
        if remove_trailing_new_line and self.at(False).type == TokenType.NewLine:
            self.tokens.pop(0)
        return self.tokens[0]
    
    def eat(self, remove_trailing_new_line: bool = False) -> Token:
        if remove_trailing_new_line and self.at(False).type == TokenType.NewLine:
            self.tokens.pop(0)
        return self.tokens.pop(0)
    
    def remove_trailing_new_lines(self) -> NoReturn:
        if self.at().type == TokenType.NewLine:
            self.eat()