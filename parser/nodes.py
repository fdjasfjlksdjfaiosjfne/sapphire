from __future__ import annotations
import typing

from parser.lexer import TokenType

class BaseNode:
    def __init__(self, *args, **kwargs):
        ann = {}
        # Collect all annotations from the class hierarchy
        for cls in reversed(self.__class__.__mro__):
            ann.update(getattr(cls, '__annotations__', {}))

        ann_keys = list(ann.keys())

        # Assign positional arguments
        if len(args) > len(ann_keys):
            raise TypeError(f"{self.__class__.__name__} expected at most {len(ann_keys)} positional arguments, got {len(args)}")
        for i, value in enumerate(args):
            setattr(self, ann_keys[i], value)

        # Assign keyword arguments, checking for duplicates and invalid keys
        for k in kwargs:
            if k not in ann:
                raise TypeError(f"{self.__class__.__name__} got an unexpected keyword argument '{k}'")
            if hasattr(self, k):
                raise TypeError(f"{self.__class__.__name__} got multiple values for argument '{k}'")
            setattr(self, k, kwargs[k])

        # Set remaining attributes to None if not already set
        for k in ann:
            if not hasattr(self, k):
                setattr(self, k, None)

class StmtNode(BaseNode):
    pass

class ExprNode(StmtNode): 
    pass

class ProgramNode(StmtNode):
    body: CodeBlockNode
    def __init__(self):
        self.body = CodeBlockNode()
    def __iter__(self):
        yield from self.body
class VarDeclarationNode(StmtNode):
    
    constant: bool

class ModifierAssignmentNode(StmtNode):
    assignee: ExprNode
    assign_oper: str
    value: ExprNode

class AssignmentNode(StmtNode):
    idents_and_expr: typing.List[ExprNode]

class WalrusNode(ExprNode):
    assignee: ExprNode
    value: ExprNode

class ReturnNode(StmtNode):
    value: ExprNode

class ConditionalNode(StmtNode):
    condition: ExprNode
    code_block: CodeBlockNode
    otherwise: CodeBlockNode | ConditionalNode | None

class WhileLoopNode(StmtNode):
    condition: ExprNode
    code_block: CodeBlockNode
    else_block: CodeBlockNode | None

class GlorifiedWhileLoopNode(StmtNode):
    init: ExprNode | VarDeclarationNode
    condition: ExprNode
    repeat: ExprNode
    code_block: CodeBlockNode
    else_block: CodeBlockNode | None

class ForLoopNode(StmtNode):
    iter_vars: list[str]
    iterable: ExprNode
    code_block: CodeBlockNode
    else_block: CodeBlockNode | None

class BreakNode(StmtNode): 
    label: str | None

class ContinueNode(StmtNode):
    label: str | None

class MatchPatternNode(BaseNode):
    pass

class ValuePattern(MatchPatternNode):
    # case 123
    # case "foo"
    # case 3.41
    # case null
    val: ExprNode

class WildcardPattern(MatchPatternNode):
    # case _
    pass

class VariablePattern(MatchPatternNode):
    # case ... as foo
    pattern: MatchPatternNode
    name: str

class SequencePattern(MatchPatternNode):
    # case [x, y, z]
    elements: list[VariablePattern | WildcardPattern | EllipsisNode]

class MappingPattern(MatchPatternNode):
    # case {"x": x}
    elements: list[tuple[ExprNode, MatchPatternNode]]

class MultipleChoicePattern(MatchPatternNode):
    # case 1, 2, 3
    elements: list[MatchPatternNode]
class CaseNode(BaseNode):
    pattern: MatchPatternNode
    guard: ExprNode | None
    body: CodeBlockNode

class MatchCaseNode(ExprNode):
    subject: ExprNode
    cases: list[tuple[MatchPatternNode, CodeBlockNode]]

class UnaryNode(ExprNode):
    expr: ExprNode
    attachment: TokenType
    position: TokenType

class BinaryNode(ExprNode):
    left: ExprNode
    oper: TokenType
    right: ExprNode

class TernaryNode(ExprNode):
    cond: ExprNode
    true: ExprNode
    false: ExprNode

class MemberAccessNode(ExprNode):
    obj: ExprNode
    attr: str

class SubscriptionNode(ExprNode):
    obj: ExprNode
    item: ExprNode

class ComparisonNode(ExprNode):
    left: ExprNode
    operators: list[TokenType]
    exprs: list[ExprNode]

class CallArgumentList(typing.NamedTuple):
    args: list[ExprNode] = []
    kwargs: dict[str, ExprNode] = {}

class CallNode(ExprNode):

    caller: ExprNode
    args: CallArgumentList

class LiteralNode(ExprNode):
    pass

class IntNode(LiteralNode):
    value: int

class FloatNode(LiteralNode):
    value: float

class StrNode(LiteralNode):
    value: str

class BoolNode(LiteralNode):
    value: bool

class NullNode(LiteralNode):
    pass

class NotImplementedNode(LiteralNode):
    pass

class EllipsisNode(LiteralNode):
    pass

class IdentifierNode(ExprNode):
    symbol: str

class ListNode(ExprNode):
    value: list[ExprNode]

class TupleNode(ExprNode):
    value: list[ExprNode]

class SetNode(ExprNode):
    value: list[ExprNode]

class DictNode(ExprNode):
    value: list[tuple[ExprNode, ExprNode]]

class ScopeBlockNode(ExprNode):
    code_block: CodeBlockNode

class CodeBlockNode(BaseNode):
    body: list
    def __init__(self):
        self.body = []
    def append(self, object: typing.Any, /):
        from backend import errors
        t = type(object)
        if BaseNode not in t.mro():
            raise errors.InternalError(t, t.mro)
        # & Fuck walrus
        elif t == WalrusNode:
            raise errors.SyntaxError("The walrus operator cannot be used in this context")
        self.body.append(object)
    def __iter__(self):
        yield from self.body
