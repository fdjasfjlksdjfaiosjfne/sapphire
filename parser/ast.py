from __future__ import annotations
from typing import *
from dataclasses import dataclass
from enum import Enum
from backend.typecheck import enforce_types

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
    Decorator = 4

class Stmt:
    @enforce_types
    def __init_subclass__(cls):
        if cls.__name__ != "Expr" and getattr(NodeType, cls.__name__).value > 0:
            cls.kind = getattr(NodeType, cls.__name__)

class Expr(Stmt): 
    @enforce_types
    def __init_subclass__(cls):
        if getattr(NodeType, cls.__name__).value < 0:
            cls.kind = getattr(NodeType, cls.__name__)

@dataclass
class Program(Stmt):
    @enforce_types
    def __init__(self, body):
        self.body = body

@dataclass
class VarDeclaration(Stmt):
    @enforce_types
    def __init__(self, assignee: Expr, oper: str, value: Expr):
        self.assignee = assignee
        self.oper = oper
        self.value = value

# @decorators...
# fn foo(x: int, y: int): float {...}

@dataclass
class FunctionDeclaration(Stmt):
    @enforce_types
    def __init__(self, name: str, args: List[DeclarationArgument], return_value: any, body: List[Stmt]):
        self.name = name
        self.args = args
        self.return_value = return_value
        self.body = List[Stmt]

@dataclass
class Decorator(Stmt):
    @enforce_types
    def __init__(self, name: str, args: List[CallArgument]):
        self.name = name
        self.args = args
@dataclass
class VarAssignmentStmt(Stmt):
    @enforce_types
    def __init__(self, assignee: Expr, oper: str, value: Expr):
        self.assignee = assignee
        self.oper = oper
        self.value = value

@dataclass
class TypeHint(Expr):
    @enforce_types
    def __init__(self, content: str):
        self.content = content

@dataclass
class DeclarationArgument(Expr):
    @enforce_types
    def __init__(self, name: str, type_hint: TypeHint):
        self.name = name
        self.type_hint = type_hint

@dataclass
class CallArgument(Expr):
    @enforce_types
    def __init__(self, *, name: str | None = None, value: Expr):
        self.name = name
        self.value = value

@dataclass
class BinaryExpr(Expr):
    @enforce_types
    def __init__(self, left: Expr, oper: str, right: Expr):
        self.left = left
        self.oper = oper
        self.right = right

@dataclass
class VarAssignmentExpr(Expr):
    @enforce_types
    def __init__(self, assignee: Expr, oper: str, value: Expr):
        self.assignee = assignee
        self.oper = oper
        self.value = value

@dataclass
class TernaryExpr(Expr):
    @enforce_types
    def __init__(self, left: Expr, true_expr: Expr, false_expr: Expr):
        self.left = left
        self.true_expr = true_expr
        self.false_expr = false_expr

@dataclass
class UnaryExpr(Expr):
    @enforce_types
    def __init__(self, expr: Expr, symbol: str):
        self.expr = expr
        self.symbol = symbol

@dataclass
class IntLiteral(Expr):
    @enforce_types
    def __init__(self, value: int):
        self.value = value

@dataclass
class FloatLiteral(Expr):
    @enforce_types
    def __init__(self, value: float):
        self.value = value

@dataclass
class StrLiteral(Expr):
    @enforce_types
    def __init__(self, value: str):
        self.value = value

@dataclass
class BoolLiteral(Expr):
    @enforce_types
    def __init__(self, value: bool):
        self.value = value

@dataclass
class NullLiteral(Expr): pass

@dataclass
class ArrayLiteral(Expr):
    @enforce_types
    def __init__(self, properties: List[Expr]):
        self.properties = properties

@dataclass
class SetLiteral(Expr):
    @enforce_types
    def __init__(self, properties: Set[Expr]):
        self.properties = properties

@dataclass
class Property(Expr):
    @enforce_types
    def __init__(self, key: Expr, value: Expr):
        self.key = key
        self.value = value

@dataclass
class MapLiteral(Expr):
    @enforce_types
    def __init__(self, properties: List[Property]):
        self.properties = properties

@dataclass
class ObjLiteral(Expr):
    @enforce_types
    def __init__(self, properties: List[Property]):
        self.properties = properties

@dataclass
class Identifier(Expr):
    @enforce_types
    def __init__(self, name: str):
        self.name = name

@dataclass
class CallExpr(Expr):
    @enforce_types
    def __init__(self, call: Expr, args: List[CallArgument]):
        self.call = call
        self.args = args

@dataclass
class MemberExpr(Expr):
    @enforce_types
    def __init__(self, obj: Expr, prop: Expr, computed: bool):
        self.obj = obj
        self.prop = prop
        self.computed = computed