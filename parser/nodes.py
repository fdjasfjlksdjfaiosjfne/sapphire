from __future__ import annotations
from abc import ABC
from typing import final, List
from enum import Enum, auto
from dataclasses import dataclass
from lexer.lexer import Token

class NodeType(Enum):
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

class Stmt(ABC):
    kind: NodeType
    @final
    def __init_subclass__(cls):
        if cls.__name__ != "Expr":
            setattr(cls, "kind", getattr(NodeType, cls.__name__.removesuffix("Node")))
    @final
    def __ne__(self, value: NodeType) -> bool:
        if isinstance(value, NodeType):
            return self.kind != value
        return NotImplemented
    @final
    def __eq__(self, value: NodeType) -> bool:
        if isinstance(value, NodeType):
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
    body: List[Stmt]
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