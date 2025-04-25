from __future__ import annotations
from typing import Any, List, Optional, NamedTuple, Dict, Literal, Union
from lexer.lexer import TokenType
class Stmt:
    pass

class Expr(Stmt): 
    pass


class Program(Stmt):
    def __init__(self):
        self.body: CodeBlock = CodeBlock()
    def __iter__(self):
        yield from self.body


class VarDeclaration(Stmt):
    def __init__(self, name: str, value: Optional[Expr] = None, constant: bool = False):
        self.name = name
        self.value = value
        self.constant = constant


class ModifierAssignment(Stmt):
    def __init__(self, assignee: Expr, assign_oper: str, value: Expr):
        self.assignee = assignee
        self.assign_oper = assign_oper
        self.value = value


class Assignment(Stmt):
    def __init__(self, idents_and_expr: List[Expr]):
        self.idents_and_expr = idents_and_expr


class Walrus(Expr):
    def __init__(self, assignee: Expr, value: Expr):
        self.assignee = assignee
        self.value = value


class Return(Stmt):
    def __init__(self, value: Expr):
        self.value = value

# x = if x == 2 { return 420 } else { return 69 }

class Conditional(Stmt):
    def __init__(self, condition: Expr, code_block: CodeBlock, otherwise: Optional[Conditional | CodeBlock] = None):
        self.condition = condition
        self.code_block = code_block
        self.otherwise = otherwise

class WhileLoop(Stmt):
    def __init__(self, condition: Expr, code_block: CodeBlock, else_block: Optional[CodeBlock] = None):
        self.condition = condition
        self.code_block = code_block
        self.else_block = else_block

# for (init; condition; repeat) {...}
class GlorifiedWhileLoop(Stmt):
    def __init__(self, init: Expr, condition: Expr, repeat: Expr, code_block: CodeBlock, else_block: Optional[CodeBlock] = None):
        self.init = init
        self.condition = condition
        self.repeat = repeat
        self.code_block = code_block
        self.else_block = else_block

# for ... in iterable {...}
class ForLoop(Stmt):
    def __init__(self, iter_vars: List[Expr], iterable: Expr, code_block: CodeBlock):
        self.iter_vars = iter_vars
        self.iterable = iterable
        self.code_block = code_block

class Break(Stmt): 
    def __init__(self, label: Optional[str] = None):
        self.label = label

class Continue(Stmt):
    def __init__(self, label: Optional[str] = None):
        self.label = label

class MatchCase(Expr):
    # This is way too complicated for now
    # TODO
    pass


class Unary(Expr):
    def __init__(self, expr: Expr, attachment: TokenType, position: Literal["Prefix", "Postfix"]):
        self.expr = expr
        self.attachment = attachment
        self.position = position


class Binary(Expr):
    def __init__(self, left: Expr, oper: TokenType, right: Expr):
        self.left = left
        self.oper = oper
        self.right = right


class Ternary(Expr):
    def __init__(self, cond: Expr, true: Expr, false: Expr):
        self.cond = cond
        self.true = true
        self.false = false


class MemberAccess(Expr):
    def __init__(self, obj: Expr, attr: str):
        self.obj = obj
        self.attr = attr


class Subscription(Expr):
    def __init__(self, obj: Expr, item: Expr):
        self.obj = obj
        self.item = item


class Comparison(Expr):
    def __init__(self, left: Expr, operators: List[TokenType], exprs: List[Expr]):
        self.left = left
        self.operators = operators
        self.exprs = exprs


class CallArgumentList(NamedTuple):
    args: List[Expr] = []
    kwargs: Dict[str, Expr] = {}


class Call(Expr):
    def __init__(self, caller: Expr, args: CallArgumentList):
        self.caller = caller
        self.args = args


class Int(Expr):
    def __init__(self, value: int):
        self.value = value


class Float(Expr):
    def __init__(self, value: float):
        self.value = value


class Str(Expr):
    def __init__(self, value: str):
        self.value = value


class Bool(Expr):
    def __init__(self, value: bool):
        self.value = value


class Null(Expr):
    def __init__(self):
        pass


class Identifier(Expr):
    def __init__(self, symbol: str):
        self.symbol = symbol


class CodeBlock(Expr):
    def __init__(self):
        self.body: list = []
    def append(self, object: Any, /):
        # Scrolling to find every subclass of Stmt and beyond
        t = type(object)
        if Stmt not in t.mro():
            raise Exception()
        elif t == Walrus:
            raise Exception()
        self.body.append(object)
    def __iter__(self):
        yield from self.body

AllExprTypeHint = Union [
    Identifier,
    Int,
    Float,
    Str,
    Bool,
    Null,
    Conditional,
    MatchCase,
    Walrus,
    Comparison,
    Unary,
    Binary,
    Ternary,
    MemberAccess,
    Subscription,
    Call,
    CodeBlock,
    Expr
]

AllStmtsTypeHint = Union[
    Stmt,
    Assignment,
    ModifierAssignment,
    Program,
    VarDeclaration,
    AllExprTypeHint
]