from __future__ import annotations
from typing import *
from dataclasses import dataclass
from enum import Enum

class NodeType(Enum):
    # ^ Exprs
    BinaryExpr = -1
    Int = -2
    Float = -3
    Str = -4
    Bool = -5
    Null = -6
    Array = -7
    Set = -8
    Map = -9
    Object = -10
    Property = -11
    VarDeclarationExpr = -12
    Argument = -13
    Ternary = -14
    Unary = -15
    Identifier = -16
    Member = -17
    # ^ Stmts
    Program = 1
    VarDeclarationStmt = 2
    FunctionDeclaration = 3

class Stmt:
    def __init_subclass__(cls):
        if cls.__name__ != "Expr" and getattr(NodeType, cls.__name__).value > 0:
            cls.kind = getattr(NodeType, cls.__name__)

class Expr(Stmt): 
    def __init_subclass__(cls):
        if getattr(NodeType, cls.__name__).value < 0:
            cls.kind = getattr(NodeType, cls.__name__)

@dataclass
class Program(Stmt):
    def __init__(self, body):
        self.body = body

@dataclass
class VarDeclaration(Stmt):
    def __init__(self, assignee: Expr, oper: str, value: Expr):
        self.assignee = assignee
        self.oper = oper
        self.value = value

# fn foo(x: int, y: int): float {...}

@dataclass
class FunctionDeclaration(Stmt):
    def __init__(self, name: str, args: List[DeclaredArgument], return_value: any, body: List[Stmt]):
        self.name = name
        self.args = args
        self.return_value = return_value
        self.body = List[Stmt]

@dataclass
class VarAssignmentStmt(Stmt):
    def __init__(self, assignee: Expr, oper: str, value: Expr):
        self.assignee = assignee
        self.oper = oper
        self.value = value

@dataclass
class DeclaredArgument(Expr):
    def __init__(self, name: str, type_hint: Expr):
        self.name = name

@dataclass
class CallArgument(Expr):
    def __init__(self, *, name: str | None = None, value: Expr):
        self.name = name
        self.value = value

@dataclass
class BinaryExpr(Expr):
    def __init__(self, left: Expr, oper: str, right: Expr):
        self.left = left
        self.oper = oper
        self.right = right

@dataclass
class VarAssignmentExpr(Expr):
    def __init__(self, assignee: Expr, oper: str, value: Expr):
        self.assignee = assignee
        self.oper = oper
        self.value = value

@dataclass
class TernaryExpr(Expr):
    def __init__(self, left: Expr, true_expr: Expr, false_expr: Expr):
        self.left = left
        self.true_expr = true_expr
        self.false_expr = false_expr

@dataclass
class UnaryExpr(Expr):
    def __init__(self, expr: Expr, symbol: str):
        self.expr = expr
        self.symbol = symbol

@dataclass
class IntLiteral(Expr):
    def __init__(self, value: int):
        self.value = value

@dataclass
class FloatLiteral(Expr):
    def __init__(self, value: float):
        self.value = value

@dataclass
class StrLiteral(Expr):
    def __init__(self, value: str):
        self.value = value

@dataclass
class BoolLiteral(Expr):
    def __init__(self, value: bool):
        self.value = value

@dataclass
class NullLiteral(Expr): pass

@dataclass
class ArrayLiteral(Expr):
    def __init__(self, properties: List[Expr]):
        self.properties = properties

@dataclass
class SetLiteral(Expr):
    def __init__(self, properties: Set[Expr]):
        self.properties = properties

@dataclass
class Property(Expr):
    def __init__(self, key: Expr, value: Expr):
        self.key = key
        self.value = value

@dataclass
class MapLiteral(Expr):
    def __init__(self, properties: List[Property]):
        self.properties = properties

@dataclass
class ObjLiteral(Expr):
    def __init__(self, properties: List[Property]):
        self.properties = properties

@dataclass
class Identifier(Expr):
    def __init__(self, name: str):
        self.name = name

@dataclass
class CallExpr(Expr):
    def __init__(self, call: Expr, args: List[CallArgument]):
        self.call = call
        self.args = args

@dataclass
class MemberExpr(Expr):
    def __init__(self, obj: Expr, prop: Expr, computed: bool):
        self.obj = obj
        self.prop = prop
        self.computed = computed