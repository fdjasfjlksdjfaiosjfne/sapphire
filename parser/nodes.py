from __future__ import annotations
import dataclasses
import enum
import typing


from parser.lexer import TokenTypeEnum

class ExprContext(enum.Enum):
    Load = 0
    Store = 1
    Del = 2

class SequencePatternType(enum.Enum):
    List = 0
    Tuple = 1
    Set = 2

@dataclasses.dataclass
class BaseASTNode:
    pass
@dataclasses.dataclass
class StmtNode(BaseASTNode):
    pass

@dataclasses.dataclass
class ExprNode(StmtNode): 
    pass

@dataclasses.dataclass
class ModuleNode(StmtNode):
    body: CodeBlockNode
    def __init__(self, body: CodeBlockNode | None = None):
        if body is None:
            self.body = CodeBlockNode()
        else:
            assert body is not None
            self.body = body
    def __iter__(self):
        yield from self.body

@dataclasses.dataclass
class VarDeclarationNode(StmtNode):
    idents: list[list[ExprNode]]
    expr: ExprNode
    constant: bool = False

class DeclaredArgumentType(enum.Enum):
    Normal = enum.auto()
    PositionalSeparator = enum.auto() # /
    KeywordSeparator = enum.auto() # *
    PositionalVariadic = enum.auto()
    KeywordVariadic = enum.auto()

@dataclasses.dataclass
class DeclaredArgumentNode(BaseASTNode):
    type: DeclaredArgumentType
    name: str | None = None

@dataclasses.dataclass
class FunctionDeclarationNode(StmtNode):
    name: str
    args: list[DeclaredArgumentNode]
    code_block: CodeBlockNode

@dataclasses.dataclass
class ModifierAssignmentNode(StmtNode):
    assignee: ExprNode
    assign_oper: str
    value: ExprNode

@dataclasses.dataclass
class AssignmentNode(StmtNode):
    targets: list[list[ExprNode]]
    value: ExprNode

@dataclasses.dataclass
class WalrusNode(ExprNode):
    assignee: ExprNode
    value: ExprNode

@dataclasses.dataclass
class ReturnNode(StmtNode):
    value: ExprNode

@dataclasses.dataclass
class ConditionalNode(StmtNode):
    condition: ExprNode
    code_block: CodeBlockNode
    otherwise: CodeBlockNode | ConditionalNode | None = None

@dataclasses.dataclass
class WhileLoopNode(StmtNode):
    condition: ExprNode
    code_block: CodeBlockNode
    else_block: CodeBlockNode | None

@dataclasses.dataclass
class GlorifiedWhileLoopNode(StmtNode):
    init: ExprNode | VarDeclarationNode | None
    condition: ExprNode
    repeat: ExprNode | None
    code_block: CodeBlockNode
    else_block: CodeBlockNode | None

@dataclasses.dataclass
class ForLoopNode(StmtNode):
    iter_vars: list[str]
    iterable: ExprNode
    code_block: CodeBlockNode
    else_block: CodeBlockNode | None

@dataclasses.dataclass
class DoWhileLoopNode(StmtNode):
    condition: ExprNode
    code_block: CodeBlockNode
    else_block: CodeBlockNode | None

@dataclasses.dataclass
class BreakNode(StmtNode): 
    label: str | None = None

@dataclasses.dataclass
class ContinueNode(StmtNode):
    label: str | None = None

@dataclasses.dataclass
class ThrowNode(StmtNode):
    error_expr: ExprNode | None = None
    cause: ExprNode | None = None

@dataclasses.dataclass
class MatchPatternNode(BaseASTNode):
    pass

@dataclasses.dataclass
class LiteralPatternNode(MatchPatternNode):
    # case 123
    # case "foo"
    # case 3.41
    # case null
    val: ExprNode

@dataclasses.dataclass
class WildcardPatternNode(MatchPatternNode):
    # case _
    pass

@dataclasses.dataclass
class VariablePatternNode(MatchPatternNode):
    # case ... as foo
    pattern: MatchPatternNode
    ident_name: str

@dataclasses.dataclass
class ClassPatternNode(MatchPatternNode):
    # case Ap(1, 3, a = 6)
    name: str
    args: list[MatchPatternNode]
    kwargs: dict[str, MatchPatternNode]

@dataclasses.dataclass
class SequencePatternNode(MatchPatternNode):
    # case [x, y, z]
    type: SequencePatternType
    elements: list[MatchPatternNode]

@dataclasses.dataclass
class MappingPatternNode(MatchPatternNode):
    # case {"x": x}
    elements: list[tuple[MatchPatternNode, MatchPatternNode]]

@dataclasses.dataclass
class MultipleChoicePatternNode(MatchPatternNode):
    # case 1, 2, 3
    elements: list[MatchPatternNode]
@dataclasses.dataclass
class CaseNode(BaseASTNode):
    pattern: MatchPatternNode
    guard: ExprNode | None
    body: CodeBlockNode

@dataclasses.dataclass
class MatchCaseNode(ExprNode):
    subject: ExprNode
    cases: list[MatchPatternNode]

@dataclasses.dataclass
class UnaryNode(ExprNode):
    expr: ExprNode
    attachment: TokenTypeEnum
    position: typing.Literal["Prefix", "Postfix"]

@dataclasses.dataclass
class BinaryNode(ExprNode):
    left: ExprNode
    oper: TokenTypeEnum
    right: ExprNode

@dataclasses.dataclass
class TernaryNode(ExprNode):
    cond: ExprNode
    true: ExprNode
    false: ExprNode

@dataclasses.dataclass
class AttributeNode(ExprNode):
    obj: ExprNode
    attr: str
    context: ExprContext = ExprContext.Load

@dataclasses.dataclass
class ClassAttributeNode(ExprNode):
    obj: ExprNode
    attr: str
    context: ExprContext = ExprContext.Load

@dataclasses.dataclass
class SubscriptionNode(ExprNode):
    obj: ExprNode
    slice: tuple[ExprNode, ExprNode | None, ExprNode | None]
    context: ExprContext | None = None

@dataclasses.dataclass
class ComparisonNode(ExprNode):
    left: ExprNode
    operators: list[TokenTypeEnum]
    exprs: list[ExprNode]

class CallArgumentList(typing.NamedTuple):
    args: list[ExprNode] = []
    kwargs: dict[str, ExprNode] = {}

@dataclasses.dataclass
class CallNode(ExprNode):
    caller: ExprNode
    args: CallArgumentList

@dataclasses.dataclass
class LiteralNode(ExprNode):
    value: typing.Any

@dataclasses.dataclass
class IntNode(LiteralNode):
    value: int

@dataclasses.dataclass
class FloatNode(LiteralNode):
    value: float

@dataclasses.dataclass
class StrNode(LiteralNode):
    value: str

@dataclasses.dataclass
class FormattedStrNode(ExprNode):
    values: list[StrNode | FormattedValue]

@dataclasses.dataclass
class FormattedValue(ExprNode):
    value: ExprNode
    conversion: int
    formatting: FormattedStrNode | None

@dataclasses.dataclass
class BoolNode(LiteralNode):
    value: bool

@dataclasses.dataclass
class NullNode(LiteralNode):
    def __init__(self, value = None):
        self.value = None

@dataclasses.dataclass
class NotImplementedNode(LiteralNode):
    pass

@dataclasses.dataclass
class EllipsisNode(LiteralNode):
    pass

@dataclasses.dataclass
class IdentifierNode(ExprNode):
    symbol: str
    context: ExprContext = ExprContext.Load

@dataclasses.dataclass
class ListNode(ExprNode):
    value: list[ExprNode]

@dataclasses.dataclass
class LoopInComprehension(BaseASTNode):
    pass

@dataclasses.dataclass
class ForLoopInComprehension(LoopInComprehension):
    var_list: list[ExprNode]
    iterable: ExprNode
    conditions: list[ExprNode]
    fallbacks: list[ExprNode | None]

@dataclasses.dataclass
class SequenceComprehensionNode(ExprNode):
    subjects: list[ExprNode]
    generators: list[LoopInComprehension]

@dataclasses.dataclass
class ListComprehensionNode(SequenceComprehensionNode): pass

@dataclasses.dataclass
class GeneratorComprehensionNode(SequenceComprehensionNode): pass
@dataclasses.dataclass
class SetComprehensionNode(SequenceComprehensionNode): pass
@dataclasses.dataclass
class TupleNode(ExprNode):
    value: list[ExprNode]
@dataclasses.dataclass
class SetNode(ExprNode):
    value: list[ExprNode]

@dataclasses.dataclass
class DictNode(ExprNode):
    value: list[tuple[ExprNode, ExprNode]]

@dataclasses.dataclass
class DictComprehensionNode(ExprNode):
    subject: list[tuple[ExprNode, ExprNode]]
    generators: list[LoopInComprehension]

@dataclasses.dataclass
class ScopeBlockNode(ExprNode):
    code_block: CodeBlockNode

@dataclasses.dataclass
class CodeBlockNode(BaseASTNode):
    body: list[BaseASTNode]
    def __init__(self, body: list | None = None):
        if body is None:
            self.body = []
        else:
            assert body is not None
            self.body = body
    def append(self, object: typing.Any, /):
        from backend import errors
        t = type(object)
        if BaseASTNode not in t.mro():
            raise errors.InternalError(t, t.mro)
        # & Fuck walrus
        elif t == WalrusNode:
            raise errors.SyntaxError("The walrus operator cannot be used in this context")
        self.body.append(object)
    def __iter__(self):
        yield from self.body
