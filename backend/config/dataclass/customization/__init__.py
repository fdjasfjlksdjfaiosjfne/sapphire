import typing
from dataclasses import dataclass

from backend.config.baseclasses import CustomDataclass, ConfigDescriptor, _UNFILLED
from backend.config.dataclass.customization.literals import *
from backend.config.dataclass.customization.control import *
from backend.config.dataclass.customization.objects import *
from backend.config.dataclass.customization.operators import *

@dataclass(frozen=True, kw_only=True)
class AnnotationsConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class OOPConfigCls(CustomDataclass):
    oop_model: ConfigDescriptor[typing.Literal["class", "prototype", "hybrid"]] = ConfigDescriptor(_UNFILLED, "class")
    forced_encapsulation: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    encapsulation_method: ConfigDescriptor[typing.Literal["disabled", "enforced", "hybrid"]] = ConfigDescriptor(_UNFILLED, "enforced")

@dataclass(frozen=True, kw_only=True)
class InlineCommentCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["#", "//", ";", "--", "%"]] = ConfigDescriptor(_UNFILLED, "#")
    space_required: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class MultilineCommentSyntaxConfigCls(CustomDataclass):
    start: ConfigDescriptor[typing.Literal["/*", "###", "#=", "#*", "(*", "<!--", "{#", "{{!--", "{{--", "--[[", "#|", "%{"]] = ConfigDescriptor(_UNFILLED, "/*")
    end: ConfigDescriptor[typing.Literal["*/", "###", "=#", "*#", "--}}", "]]", "|#", "}%"]] = ConfigDescriptor(_UNFILLED, "*/")

@dataclass(frozen=True, kw_only=True)
class MultilineCommentConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[MultilineCommentSyntaxConfigCls] = ConfigDescriptor(_UNFILLED, MultilineCommentSyntaxConfigCls())

@dataclass(frozen=True, kw_only=True)
class CommentConfigCls(CustomDataclass):
    inline_comment: ConfigDescriptor[InlineCommentCls] = ConfigDescriptor(_UNFILLED, InlineCommentCls())
    multiline_comment: ConfigDescriptor[MultilineCommentConfigCls] = ConfigDescriptor(_UNFILLED, MultilineCommentConfigCls())

@dataclass(frozen=True, kw_only=True)
class VariablesConfigCls(CustomDataclass):
    implicit_globals: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, False)
    function_hoisting: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class UncategorizedConfigCls(CustomDataclass):
    implicit_return: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, False)
    trailing_comma: ConfigDescriptor[typing.Literal["always", "never", "single_tuple_only"]] = ConfigDescriptor(_UNFILLED, "always")
    semicolon_required: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, False)
    soft_keywords: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, False)
    code_blocks: ConfigDescriptor[typing.Literal["indentation", "braces", "end"]] = ConfigDescriptor(_UNFILLED, "braces")
    mutable_value_assignment_behavior: ConfigDescriptor[typing.Literal["copy", "reference"]] = ConfigDescriptor(_UNFILLED, "copy")

@dataclass(frozen=True, kw_only=True)
class CustomizationConfigCls(CustomDataclass):
    annotations: ConfigDescriptor[AnnotationsConfigCls] = ConfigDescriptor(_UNFILLED, AnnotationsConfigCls())
    literals: ConfigDescriptor[LiteralsConfigCls] = ConfigDescriptor(_UNFILLED, LiteralsConfigCls())
    comments: ConfigDescriptor[CommentConfigCls] = ConfigDescriptor(_UNFILLED, CommentConfigCls())
    control_flow: ConfigDescriptor[ControlFlowConfigCls] = ConfigDescriptor(_UNFILLED, ControlFlowConfigCls())
    variables: ConfigDescriptor[VariablesConfigCls] = ConfigDescriptor(_UNFILLED, VariablesConfigCls())
    objects: ConfigDescriptor[ObjectsConfigCls] = ConfigDescriptor(_UNFILLED, ObjectsConfigCls())
    oop: ConfigDescriptor[OOPConfigCls] = ConfigDescriptor(_UNFILLED, OOPConfigCls())
    operators: ConfigDescriptor[OperatorsConfigCls] = ConfigDescriptor(_UNFILLED, OperatorsConfigCls())
    uncategorized: ConfigDescriptor[UncategorizedConfigCls] = ConfigDescriptor(_UNFILLED, UncategorizedConfigCls())