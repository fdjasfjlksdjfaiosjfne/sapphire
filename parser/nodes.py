from __future__ import annotations
from abc import ABC
from typing import final, List, Optional
from enum import Enum, auto
from dataclasses import dataclass
from lexer.lexer import Token

class NT(Enum):
    Program = auto()
    Return = auto()
    Assignment = auto()
    WalrusExpr = auto()
    Int = auto()
    Float = auto()
    Str = auto()
    Bool = auto()
    Null = auto()
    Identifier = auto()
    BinaryExpr = auto()
    CodeBlock = auto()
    Ternary = auto()
    Comparison = auto()
    WhileLoop = auto()
    ForLoop = auto()
    MatchCase = auto()
    Conditional = auto()

class Stmt(ABC):
    kind: NT
    @final
    def __init_subclass__(cls):
        if cls.__name__ != "Expr":
            setattr(cls, "kind", getattr(NT, cls.__name__.removesuffix("Node")))
    @final
    def __ne__(self, value: NT) -> bool:
        if isinstance(value, NT):
            return self.kind != value
        return NotImplemented
    @final
    def __eq__(self, value: NT) -> bool:
        if isinstance(value, NT):
            return self.kind == value
        return NotImplemented

class Expr(Stmt): pass

@dataclass(eq = False)
class ProgramNode(Stmt):
    body: CodeBlockNode
    def __iter__(self):
        yield iter(self.body)

@dataclass(eq = False)
class AssignmentNode(Stmt):
    assignee: Expr
    assign_oper: str
    value: Expr

@dataclass(eq = False)
class ReturnNode(Stmt):
    value: Expr

# x = if x == 2 { return 420 } else { return 69 }
@dataclass(eq = False)
class ConditionalNode(Expr):
    condition: Expr
    code_block: CodeBlockNode
    otherwise: Optional[ConditionalNode | CodeBlockNode] = None

@dataclass(eq = False)
class MatchCaseNode(Expr):
    # This is way too complicated for now
    # TODO
    pass

@dataclass(eq = False)
class TernaryNode(Expr):
    cond: Expr
    true: Expr
    false: Expr

@dataclass(eq = False)
class ComparisonNode(Expr):
    left: Expr
    operators: List[Token]
    exprs: List[Expr]

@dataclass(eq = False)
class WalrusExprNode(AssignmentNode, Expr):
    pass

@dataclass(eq = False)
class BinaryExprNode(Expr):
    left: Expr
    oper: Token
    right: Expr

@dataclass(eq = False)
class IntNode(Expr):
    value: int

@dataclass(eq = False)
class FloatNode(Expr):
    value: float

@dataclass(eq = False)
class StrNode(Expr):
    value: str

@dataclass(eq = False)
class BoolNode(Expr):
    value: bool

@dataclass(eq = False)
class NullNode(Expr): pass

@dataclass(eq = False)
class IdentifierNode(Expr):
    symbol: str

@dataclass(eq = False)
class CodeBlockNode(Expr):
    def __init__(self):
        self.body: List[Stmt] = []
    def append(self, object: Stmt, /):
        # Scrolling to find every subclass of Stmt and beyond
        t = type(object)
        if Stmt not in t.mro():
            raise Exception()
        elif t == WalrusExprNode:
            raise Exception()
        self.body.append(object)
    def __iter__(self):
        yield from self.body