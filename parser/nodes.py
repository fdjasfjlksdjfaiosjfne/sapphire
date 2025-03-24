from __future__ import annotations
from abc import ABC
from typing import final, List, Optional, NamedTuple, Dict, Literal, Union
from enum import Enum, auto
from dataclasses import dataclass
from lexer.lexer import TokenType as TokenType

class NodeType(Enum):
    Program = auto()
    Return = auto()
    VarDeclaration = auto()
    ModifierAssignment = auto()
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
    Unary = auto()
    Call = auto()
    Subscription = auto() # a[b]
    MemberAccess = auto() # a.b

class Stmt(ABC):
    kind: NodeType
    @final
    def __init_subclass__(cls):
        if cls.__name__ != "Expr":
            setattr(cls, "kind", getattr(NodeType, cls.__name__))
    @final
    def __ne__(self, value) -> bool:
        if isinstance(value, NodeType):
            return self.kind != value
        return NotImplemented
    @final
    def __eq__(self, value) -> bool:
        if isinstance(value, NodeType):
            return self.kind == value
        return NotImplemented

class Expr(Stmt): pass

@dataclass(eq = False)
class Program(Stmt):
    def __init__(self):
        self.body: CodeBlock = CodeBlock()
    def __iter__(self):
        yield iter(self.body)

@dataclass(eq = False)
class VarDeclaration(Stmt):
    name: str
    value: Optional[Expr] = None
    constant: bool = False

@dataclass(eq = False)
class ModifierAssignment(Stmt):
    assignee: Expr
    assign_oper: str
    value: Expr

@dataclass(eq = False)
class Assignment(Stmt):
    idents_and_expr: List[Expr]

@dataclass(eq = False)
class WalrusExpr(Expr):
    assignee: Expr
    value: Expr

@dataclass(eq = False)
class Return(Stmt):
    value: Expr

# x = if x == 2 { return 420 } else { return 69 }
@dataclass(eq = False)
class Conditional(Stmt):
    condition: Expr
    code_block: CodeBlock
    otherwise: Optional[Conditional | CodeBlock] = None

@dataclass(eq = False)
class MatchCase(Expr):
    # This is way too complicated for now
    # TODO
    pass

@dataclass(eq = False)
class Unary(Expr):
    expr: Expr
    attachment: TokenType
    position: Literal["Prefix", "Postfix"]

@dataclass(eq = False)
class Binary(Expr):
    left: Expr
    oper: TokenType
    right: Expr

@dataclass(eq = False)
class Ternary(Expr):
    cond: Expr
    true: Expr
    false: Expr

@dataclass(eq = False)
class MemberAccess(Expr):
    obj: Expr
    attr: str

@dataclass(eq = False)
class Subscription(Expr):
    obj: Expr
    item: Expr
@dataclass(eq = False)
class Comparison(Expr):
    left: Expr
    operators: List[TokenType]
    exprs: List[Expr]

class CallArgumentList(NamedTuple):
    args: List[Expr] = []
    kwargs: Dict[str, Expr] = {}

@dataclass(eq = False)
class Call(Expr):
    caller: Expr
    # print("Hey there!", end = "")
    args: CallArgumentList

@dataclass(eq = False)
class Int(Expr):
    value: int

@dataclass(eq = False)
class Float(Expr):
    value: float

@dataclass(eq = False)
class Str(Expr):
    value: str

@dataclass(eq = False)
class Bool(Expr):
    value: bool

@dataclass(eq = False)
class Null(Expr): pass

@dataclass(eq = False)
class Identifier(Expr):
    symbol: str

@dataclass(eq = False)
class CodeBlock(Expr):
    def __init__(self):
        self.body: List[AllStmtsTypeHint] = []
    def append(self, object: AllStmtsTypeHint, /):
        # Scrolling to find every subclass of Stmt and beyond
        t = type(object)
        if Stmt not in t.mro():
            raise Exception()
        elif t == WalrusExpr:
            raise Exception()
        self.body.append(object)
    def __iter__(self):
        yield from self.body

AllExprTypeHint = Union[
    Identifier,
    Int,
    Float,
    Str,
    Bool,
    Null,
    Conditional,
    MatchCase,
    WalrusExpr,
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