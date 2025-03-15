from __future__ import annotations
from abc import ABC
from typing import *
from enum import Enum, auto
from dataclasses import dataclass
from lexer.lexer import Token

class NodeType(Enum):
    Program = auto()
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

class Stmt(ABC):
    kind: NodeType
    @final
    def __init_subclass__(cls):
        if cls.__name__ != "Expr":
            setattr(cls, "kind", getattr(NodeType, cls.__name__.removesuffix("Node")))

class Expr(Stmt): pass

@dataclass
class ProgramNode(Stmt):
    body: CodeBlock

@dataclass
class AssignmentNode(Stmt):
    assignee: Expr
    assign_oper: str
    value: Expr

@dataclass
class WalrusExprNode(AssignmentNode, Expr):
    pass

@dataclass
class BinaryExprNode(Expr):
    left: Expr
    oper: Token
    right: Expr

@dataclass
class IntNode(Expr):
    value: int

@dataclass
class FloatNode(Expr):
    value: float

@dataclass
class StrNode(Expr):
    value: str

@dataclass
class BoolNode(Expr):
    value: bool

@dataclass
class NullNode(Expr): pass

@dataclass
class IdentifierNode(Expr):
    name: str

@dataclass
class CodeBlock(Expr):
    body: List[str]
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