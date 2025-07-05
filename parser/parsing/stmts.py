import typing

from backend import errors
from parser.lexer import Token, TokenType
from parser.parser import eat
import parser.nodes as Nodes
from parser.parsing.exprs import parse_expr

def parse_stmt(tokens: list[Token], /, **context) -> Nodes.StmtNode:
    match tokens[0]:
        case TokenType.Let | TokenType.Const:
            return parse_var_declaration(tokens, **context)
        case TokenType.If:
            return parse_if_elif_else(tokens, clause = TokenType.If, **context)
        case TokenType.While:
            return parse_while_stmt(tokens, **context)
        case TokenType.For:
            return parse_for_stmt(tokens, **context)
        case TokenType.Break:
            # todo add label support
            return Nodes.BreakNode()
        case TokenType.Continue:
            # todo add label support
            return Nodes.ContinueNode()
        case TokenType.Scope:
            eat(tokens)
            return Nodes.ScopeBlockNode(parse_attached_code_block(tokens, **context))
        case TokenType.Match:
            return parse_match_case_stmt(tokens, **context)
        case TokenType.Return:
            eat(tokens)
            return Nodes.ReturnNode(parse_expr(tokens, allow_implicit_tuples = True, **context))
        case _:
            return parse_assignment_stmt(tokens, **context)

def parse_var_declaration(tokens: list[Token], /, **context) -> Nodes.VarDeclarationNode:
    constant = eat(tokens) == TokenType.Const
    names = parse_expr(tokens, allow_implicit_tuples = True, **context)
    if tokens[0] == TokenType.AssignOper:
        eat(tokens)
        value = parse_expr(tokens, allow_implicit_tuples = True, **context)
    else:
        value = None
    return Nodes.VarDeclarationNode(name, value, constant) # type: ignore

@typing.overload
def parse_if_elif_else(tokens: list[Token], /, clause: typing.Literal[TokenType.If, TokenType.Elif], **context) -> Nodes.ConditionalNode: ...

@typing.overload
def parse_if_elif_else(tokens: list[Token], /, clause: typing.Literal[TokenType.Else], **context) -> Nodes.CodeBlockNode: ...

def parse_if_elif_else(tokens, /, **context):
    # $ This function parses the if-elif-else
    eat(tokens, context["clause"])
    
    if context["clause"] != TokenType.Else:
        cond = parse_expr(tokens, **context)
    
    code = parse_attached_code_block(tokens, **context)
    
    # $ At this point, we're done with parsing the clause itself
    # $ Now we're checking on continuity
    
    # ? This checks on the `else`
    # ? If it is, just return the code block
    # ? Without any attempt at continuation
    if context["clause"] == TokenType.Else:
        return code

    # $ At this point, the block we're parsing should be a if/elif block
    # $ Since they can be connected with another elif or else clause
    # $ Continue to look for it
    
    # ? Check if there's any other connectable clause (elif/else) behind
    if tokens[0] in {TokenType.Elif, TokenType.Else}:
        return Nodes.ConditionalNode(cond, code, parse_if_elif_else(tokens, clause = tokens[0].type, **context))
    return Nodes.ConditionalNode(cond, code)

def parse_match_case_stmt(tokens: list[Token], /, **context) -> Nodes.MatchCaseNode:
    eat(tokens, TokenType.Match)
    subject = parse_expr(tokens, **context)


def parse_while_stmt(tokens: list[Token], /, **context) -> Nodes.WhileLoopNode:
    eat(tokens, TokenType.While)
    cond = parse_expr(tokens, **context)
    
    code = parse_attached_code_block(tokens, **context)
    els = None
    # $ Check for an `else` attachment
    if tokens == TokenType.Else:
        eat(tokens, TokenType.Else)
        els = parse_attached_code_block(tokens, **context)
    
    return Nodes.WhileLoopNode(cond, code, els)

def parse_for_stmt(tokens: list[Token], /, **context) -> Nodes.ForLoopNode:
    eat(tokens, TokenType.For)
    # & Not my proudest work...
    e = parse_expr(tokens, allow_implicit_tuples = True, **context)
    iter_vars = []
    iterable = None

    if isinstance(e, Nodes.BinaryNode) and e.oper == TokenType.In:
        if isinstance(e.left, Nodes.IdentifierNode):
            iter_vars = [e.left.symbol]
            iterable = e.right
        elif isinstance(e.left, Nodes.TupleNode):
            if all(isinstance(i, Nodes.IdentifierNode) for i in e.left.value):
                iter_vars = [i.symbol for i in e.left.value]
                iterable = e.right
            else:
                raise errors.SyntaxError("Expected only identifiers on the left-hand side of 'in'")
        else:
            raise errors.SyntaxError("Invalid iterable unpacking target before 'in'")

    elif isinstance(e, Nodes.TupleNode):
        if not e.value:
            raise errors.SyntaxError("Empty tuple is not valid in a for loop")
        
        *left, last = e.value
        if (
            isinstance(last, Nodes.BinaryNode) and last.oper == TokenType.In and
            isinstance(last.left, Nodes.IdentifierNode) and
            all(isinstance(i, Nodes.IdentifierNode) for i in left)
        ):
            iter_vars = [i.symbol for i in left] + [last.left.symbol]
            iterable = last.right
        else:
            raise errors.SyntaxError("Could not resolve iterable expression from tuple pattern")

    else:
        raise errors.SyntaxError("Invalid syntax in 'for' loop head")

    # ^ Sane part
    code_block = parse_attached_code_block(tokens, **context)
    else_block = None
    if tokens[0] == TokenType.Else:
        eat(tokens)
        else_block = parse_attached_code_block(tokens, **context)
    return Nodes.ForLoopNode(iter_vars, iterable, code_block, else_block)

def parse_assignment_stmt(tokens: list[Token], /, **context) -> Nodes.AssignmentNode:
    lhs = parse_expr(tokens, **context)
    match tokens[0]:
        case TokenType.AssignOper:
            exprs = [lhs]
            while tokens[0] == TokenType.AssignOper:
                eat(tokens)
                exprs.append(parse_expr(tokens, **context))
            return Nodes.AssignmentNode(exprs)
        case TokenType.ModifierAssignOper:
            return Nodes.ModifierAssignmentNode(lhs, eat(tokens).value, parse_expr(tokens, **context))
    return lhs

def parse_attached_code_block(tokens: list[Token], /, **context) -> Nodes.CodeBlockNode:
    # ^ Create a code block
    code = Nodes.CodeBlockNode()
    opening_token = context.pop("opening_token", TokenType.OpenCurlyBrace)
    closing_token = context.pop("closing_token", TokenType.CloseCurlyBrace)
    # $ If the code block uses {}
    if tokens[0] == opening_token:
        eat(tokens, opening_token)
        
        # Do-while loop
        while True:
            code.append(parse_stmt(tokens, **context))
            if tokens[0] == closing_token:
                break
            eat(tokens, TokenType.NewLine, TokenType.Semicolon)
        eat(tokens, closing_token)
    elif context.pop("disable_single_line_code_blocks", False):
        # $ The code block doesn't use {}
        code.append(parse_stmt(tokens, **context))
    
    return code