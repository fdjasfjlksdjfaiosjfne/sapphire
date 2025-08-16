import typing
from dataclasses import dataclass

from backend.config.dataclass.customization.literals import LiteralsCls

@dataclass(frozen=True, kw_only=True)
class AnnotationsCls:
    enabled: bool | object = True

@dataclass(frozen=True, kw_only=True)
class OOPCls:
    pass

class CommentCls: pass
class ControlFlowCls: pass
class VariablesCls: pass
class OperatorsCls: pass
class UncategorizedCls: pass

@dataclass(frozen=True, kw_only=True)
class CustomizationConfigCls:
    annotations: AnnotationsCls = AnnotationsCls()
    literals: LiteralsCls = LiteralsCls()
    comments: CommentCls
    control_flow: ControlFlowCls
    variables: VariablesCls
    oop: OOPCls = OOPCls()
    operators: OperatorsCls
    uncategorized: UncategorizedCls