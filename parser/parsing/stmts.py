import typing

from parser.lexer import Token, TokenType
from parser.parser import eat
import parser.nodes as Nodes
from parser.parsing.exprs import parse_expr

def parse_stmts(tokens: typing.List[Token]) -> Nodes.Stmt:
    match tokens[0]:
        case TokenType.Let | TokenType.Const:
            return parse_var_declaration(tokens)
        case TokenType.If:
            return parse_if_elif_else(tokens, TokenType.If)
        case TokenType.While:
            return parse_while_stmt(tokens)
        case TokenType.For:
            return parse_for_stmt(tokens)
        case TokenType.Break:
            # todo add label support
            return Nodes.BreakNode()
        case TokenType.Continue:
            # todo add label support
            return Nodes.ContinueNode()
        case TokenType.Scope:
            eat(tokens)
            
        case _:
            return parse_assignment_stmt(tokens)

def parse_var_declaration(tokens: typing.List[Token]) -> Nodes.VarDeclarationNode:
    constant = eat(tokens) == TokenType.Const
    name = eat(tokens, TokenType.Identifier).value
    if tokens[0] == TokenType.AssignOper:
        eat(tokens)
        value = parse_expr(tokens)
    else:
        value = None
    return Nodes.VarDeclarationNode(name, value, constant) # type: ignore

@typing.overload
def parse_if_elif_else(tokens: typing.List[Token], clause: typing.Literal[TokenType.If, TokenType.Elif]) -> Nodes.ConditionalNode: ...

@typing.overload
def parse_if_elif_else(tokens: typing.List[Token], clause: typing.Literal[TokenType.Else]) -> Nodes.CodeBlock: ...

def parse_if_elif_else(tokens, clause):
    # $ This function parses the if-elif-else
    eat(tokens, clause)
    
    if clause != TokenType.Else:
        cond = parse_expr(tokens)
    
    code = parse_attached_code_block(tokens)
    
    # $ At this point, we're done with parsing the clause itself
    # $ Now we're checking on the continuity
    
    # ? This checks on the `else`
    # ? If it is, just return the code block
    # ? Without any attempt at continuation
    if clause == TokenType.Else:
        return code

    # $ At this point, the block we're parsing should be a if/elif block
    # $ Since they can be connected with another elif or else clause
    # $ Continue to look for it
    
    # ? Check if there's any other connectable clause (elif/else) behind
    if tokens[0] in {TokenType.Elif, TokenType.Else}:
        return Nodes.ConditionalNode(cond, code, parse_if_elif_else(tokens, tokens[0].type))
    return Nodes.ConditionalNode(cond, code)

def parse_while_stmt(tokens: typing.List[Token]) -> Nodes.WhileLoopNode:
    eat(tokens, TokenType.While)
    cond = parse_expr(tokens)
    
    code = parse_attached_code_block(tokens)
    els = None
    # $ Check for an `else` attachment
    if tokens == TokenType.Else:
        eat(tokens, TokenType.Else)
        els = parse_attached_code_block(tokens)
    
    return Nodes.WhileLoopNode(cond, code, els)

def parse_for_stmt(tokens: list[Token]) -> Nodes.ForLoop:
    eat(tokens, TokenType.For)
    ...


def parse_assignment_stmt(tokens: list[Token]) -> Nodes.AssignmentNode:
    lhs = parse_expr(tokens)
    match tokens[0]:
        case TokenType.AssignOper:
            exprs = [lhs]
            while tokens[0] == TokenType.AssignOper:
                eat(tokens)
                exprs.append(parse_expr(tokens))
            return Nodes.AssignmentNode(exprs)
        case TokenType.ModifierAssignOper:
            return Nodes.ModifierAssignmentNode(lhs, eat(tokens).value, parse_expr(tokens))
    return lhs

def parse_attached_code_block(tokens: typing.List[Token]) -> Nodes.CodeBlock:
    # ^ Create a code block
    code = Nodes.CodeBlock()
    
    # ? If the code block uses {}
    if tokens[0] == TokenType.OpenCurlyBrace:
        eat(tokens, TokenType.OpenCurlyBrace)
        
        # Idk
        while True:
            code.append(parse_stmts(tokens))
            if tokens[0] == TokenType.CloseCurlyBrace:
                break
            eat(tokens, TokenType.NewLine, TokenType.Semicolon)
        eat(tokens, TokenType.CloseCurlyBrace)
    else:
        # ? If the code block doesn't use {}
        code.append(parse_stmts(tokens))
    
    return code