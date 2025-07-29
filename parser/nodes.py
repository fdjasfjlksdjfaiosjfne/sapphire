from __future__ import annotations
import typing
import enum

from parser.lexer.lexer import TokenType

class ExprContext(enum.Enum):
    Load = 0
    Store = 1
    Del = 2

class SequencePatternType(enum.Enum):
    List = 0
    Tuple = 1
    Set = 2

class BaseASTNode:
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
    
    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.__dict__ != other.__dict__
        return True

class StmtNode(BaseASTNode):
    pass

class ExprNode(StmtNode): 
    pass

class ModuleNode(StmtNode):
    body: CodeBlockNode
    def __init__(self, body: CodeBlockNode | None = None):
        if self.body is None:
            self.body = CodeBlockNode()
        else:
            assert body is not None
            self.body = body
    def __iter__(self):
        yield from self.body

class VarDeclarationNode(StmtNode):
    idents: list[ExprNode]
    expr: ExprNode
    constant: bool

class FunctionDeclarationNode(StmtNode):
    name: str
    args: list[ExprNode | typing.Literal[TokenType.SY_TrueDivision, TokenType.SY_Asterisk]]
    code_block: CodeBlockNode

class ModifierAssignmentNode(StmtNode):
    assignee: ExprNode
    assign_oper: str
    value: ExprNode

class AssignmentNode(StmtNode):
    targets: list[ExprNode]
    value: ExprNode

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

class DoWhileLoopNode(StmtNode):
    condition: ExprNode
    code_block: CodeBlockNode
    else_block: CodeBlockNode | None

class BreakNode(StmtNode): 
    label: str | None

class ContinueNode(StmtNode):
    label: str | None

class ThrowNode(StmtNode):
    error_expr: ExprNode | None
    cause: ExprNode | None

class MatchPatternNode(BaseASTNode):
    pass

class LiteralPatternNode(MatchPatternNode):
    # case 123
    # case "foo"
    # case 3.41
    # case null
    val: ExprNode

class WildcardPatternNode(MatchPatternNode):
    # case _
    pass

class VariablePatternNode(MatchPatternNode):
    # case ... as foo
    pattern: MatchPatternNode
    ident_name: str

class ClassPatternNode(MatchPatternNode):
    # case Ap(1, 3, a = 6)
    name: str
    args: list[MatchPatternNode]
    kwargs: dict[str, MatchPatternNode]

class SequencePatternNode(MatchPatternNode):
    # case [x, y, z]
    type: SequencePatternType
    elements: list[VariablePatternNode | WildcardPatternNode | EllipsisNode]

class MappingPatternNode(MatchPatternNode):
    # case {"x": x}
    elements: list[tuple[ExprNode, MatchPatternNode]]

class MultipleChoicePatternNode(MatchPatternNode):
    # case 1, 2, 3
    elements: list[MatchPatternNode]
class CaseNode(BaseASTNode):
    pattern: MatchPatternNode
    guard: ExprNode | None
    body: CodeBlockNode

class MatchCaseNode(ExprNode):
    subject: ExprNode
    cases: list[MatchPatternNode]

class UnaryNode(ExprNode):
    expr: ExprNode
    attachment: TokenType
    position: typing.Literal["Prefix", "Postfix"]

class BinaryNode(ExprNode):
    left: ExprNode
    oper: TokenType
    right: ExprNode

class TernaryNode(ExprNode):
    cond: ExprNode
    true: ExprNode
    false: ExprNode

class AttributeNode(ExprNode):
    obj: ExprNode
    attr: str
    context: ExprContext

class SubscriptionNode(ExprNode):
    obj: ExprNode
    slice: tuple[ExprNode, ExprNode | None, ExprNode | None]
    context: ExprContext

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
    value: typing.Any

class IntNode(LiteralNode):
    value: int

class FloatNode(LiteralNode):
    value: float

class StrNode(LiteralNode):
    value: str

class FormattedStrNode(ExprNode):
    values: list[StrNode | FormattedValue]

class FormattedValue(ExprNode):
    value: ExprNode
    conversion: int
    formatting: FormattedStrNode | None

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
    context: ExprContext

class ListNode(ExprNode):
    value: list[ExprNode]

class LoopInComprehension(BaseASTNode):
    pass

class ForLoopInComprehension(LoopInComprehension):
    var_list: list[ExprNode]
    iterable: ExprNode
    conditions: list[ExprNode]
    fallbacks: list[ExprNode | None]

class SequenceComprehensionNode(ExprNode):
    subjects: list[ExprNode]
    generators: list[LoopInComprehension]

class ListComprehensionNode(SequenceComprehensionNode): pass
class GeneratorComprehensionNode(SequenceComprehensionNode): pass
class SetComprehensionNode(SequenceComprehensionNode): pass
class TupleNode(ExprNode):
    value: list[ExprNode]
class SetNode(ExprNode):
    value: list[ExprNode]

class DictNode(ExprNode):
    value: list[tuple[ExprNode, ExprNode]]

class DictComprehensionNode(ExprNode):
    subject: tuple[ExprNode, ExprNode]
    generators: list[LoopInComprehension]

class ScopeBlockNode(ExprNode):
    code_block: CodeBlockNode

class CodeBlockNode(BaseASTNode):
    body: list
    def __init__(self, body: list | None = None):
        if self.body is None:
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
