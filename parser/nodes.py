from __future__ import annotations
import typing
from parser.lexer import TokenType

class Stmt:
    pass

class Expr(Stmt): 
    pass


class ProgramNode(Stmt):
    def __init__(self):
        self.body: CodeBlock = CodeBlock()
    def __iter__(self):
        yield from self.body


class VarDeclarationNode(Stmt):
    def __init__(self, name: str, value: typing.Optional[Expr] = None, constant: bool = False):
        self.name = name
        self.value = value
        self.constant = constant


class ModifierAssignmentNode(Stmt):
    def __init__(self, assignee: Expr, assign_oper: str, value: Expr):
        self.assignee = assignee
        self.assign_oper = assign_oper
        self.value = value


class AssignmentNode(Stmt):
    def __init__(self, idents_and_expr: typing.List[Expr]):
        self.idents_and_expr = idents_and_expr


class WalrusNode(Expr):
    def __init__(self, assignee: Expr, value: Expr):
        self.assignee = assignee
        self.value = value


class Return(Stmt):
    def __init__(self, value: Expr):
        self.value = value

class ConditionalNode(Stmt):
    def __init__(self, condition: Expr, code_block: CodeBlock, otherwise: typing.Optional[ConditionalNode | CodeBlock] = None):
        self.condition = condition
        self.code_block = code_block
        self.otherwise = otherwise

class WhileLoopNode(Stmt):
    def __init__(self, condition: Expr, code_block: CodeBlock, else_block: typing.Optional[CodeBlock] = None):
        self.condition = condition
        self.code_block = code_block
        self.else_block = else_block

# for (init; condition; repeat) {...}
class GlorifiedWhileLoopNode(Stmt):
    def __init__(self, init: Expr, condition: Expr, repeat: Expr, code_block: CodeBlock, else_block: typing.Optional[CodeBlock] = None):
        self.init = init
        self.condition = condition
        self.repeat = repeat
        self.code_block = code_block
        self.else_block = else_block

# for ... in iterable {...}
class ForLoop(Stmt):
    def __init__(self, iter_vars: list[str], iterable: Expr, code_block: CodeBlock):
        self.iter_vars = iter_vars
        self.iterable = iterable
        self.code_block = code_block

class BreakNode(Stmt): 
    def __init__(self, label: typing.Optional[str] = None):
        self.label = label

class ContinueNode(Stmt):
    def __init__(self, label: typing.Optional[str] = None):
        self.label = label

class MatchCase(Expr):
    # This is way too complicated for now
    # TODO
    pass


class UnaryNode(Expr):
    def __init__(self, expr: Expr, attachment: TokenType, position: typing.Literal["Prefix", "Postfix"]):
        self.expr = expr
        self.attachment = attachment
        self.position = position


class BinaryNode(Expr):
    def __init__(self, left: Expr, oper: TokenType, right: Expr):
        self.left = left
        self.oper = oper
        self.right = right


class TernaryNode(Expr):
    def __init__(self, cond: Expr, true: Expr, false: Expr):
        self.cond = cond
        self.true = true
        self.false = false


class MemberAccessNode(Expr):
    def __init__(self, obj: Expr, attr: str):
        self.obj = obj
        self.attr = attr


class SubscriptionNode(Expr):
    def __init__(self, obj: Expr, item: Expr):
        self.obj = obj
        self.item = item


class ComparisonNode(Expr):
    def __init__(self, left: Expr, operators: typing.List[TokenType], exprs: typing.List[Expr]):
        self.left = left
        self.operators = operators
        self.exprs = exprs


class CallArgumentList(typing.NamedTuple):
    args: typing.List[Expr] = []
    kwargs: typing.Dict[str, Expr] = {}


class CallNode(Expr):
    def __init__(self, caller: Expr, args: CallArgumentList):
        self.caller = caller
        self.args = args


class IntNode(Expr):
    def __init__(self, value: int):
        self.value = value


class FloatNode(Expr):
    def __init__(self, value: float):
        self.value = value


class StrNode(Expr):
    def __init__(self, value: str):
        self.value = value


class BoolNode(Expr):
    def __init__(self, value: bool):
        self.value = value


class NullNode(Expr):
    def __init__(self):
        pass


class IdentifierNode(Expr):
    def __init__(self, symbol: str):
        self.symbol = symbol

class ListNode(Expr):
    def __init__(self, list: list[Expr]):
        self.list = list

class TupleNode(Expr):
    def __init__(self, tple: list[Expr]):
        self.tple = tple

class SetNode(Expr):
    def __init__(self, st: list[Expr]):
        self.st = st

class ScopeBlock(Expr):
    def __init__(self, code_block: CodeBlock):
        self.code_block = code_block

class CodeBlock(Expr):
    def __init__(self):
        self.body: list = []
    def append(self, object: typing.Any, /):
        # Scrolling to find every subclass of Stmt and beyond
        t = type(object)
        if Stmt not in t.mro():
            raise Exception()
        elif t == WalrusNode:
            raise Exception()
        self.body.append(object)
    def __iter__(self):
        yield from self.body
