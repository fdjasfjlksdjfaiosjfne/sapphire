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
    syntax: ConfigDescriptor[typing.Literal["#", "//", ";", "--", "%", "::"]] = ConfigDescriptor(_UNFILLED, "#")
    space_required: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class MultilineCommentSyntaxConfigCls(CustomDataclass):
    start: ConfigDescriptor[typing.Literal["/*", "###", "#=", "#*", "(*", "<!--", "{#", "{{!--", "{{--", "--[[", "#|", "%{"]] = ConfigDescriptor(_UNFILLED, "/*")
    end: ConfigDescriptor[typing.Literal["*/", "###", "=#", "*#", "--}}", "]]", "|#", "}%"]] = ConfigDescriptor(_UNFILLED, "*/")

@dataclass(frozen=True, kw_only=True)
class MultilineCommentConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: MultilineCommentSyntaxConfigCls = MultilineCommentSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class CommentConfigCls(CustomDataclass):
    inline_comment: InlineCommentCls = InlineCommentCls()
    multiline_comment: MultilineCommentConfigCls = MultilineCommentConfigCls()

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
    annotations: AnnotationsConfigCls = AnnotationsConfigCls()
    literals: LiteralsConfigCls = LiteralsConfigCls()
    comments: CommentConfigCls = CommentConfigCls()
    control_flow: ControlFlowConfigCls = ControlFlowConfigCls()
    variables: VariablesConfigCls = VariablesConfigCls()
    objects: ObjectsConfigCls = ObjectsConfigCls()
    oop: OOPConfigCls = OOPConfigCls()
    operators: OperatorsConfigCls = OperatorsConfigCls()
    uncategorized: UncategorizedConfigCls = UncategorizedConfigCls()