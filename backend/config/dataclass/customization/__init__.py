import typing
from dataclasses import dataclass

from backend.config.baseclasses import CustomDataclass
from backend.config.dataclass.customization.literals import *
from backend.config.dataclass.customization.control import *
from backend.config.dataclass.customization.objects import *
from backend.config.dataclass.customization.operators import *

@dataclass(frozen=True, kw_only=True)
class AnnotationsConfigCls(CustomDataclass):
    enabled: bool = True


@dataclass(frozen=True, kw_only=True)
class OOPConfigCls(CustomDataclass):
    oop_model: typing.Literal["class", "prototype", "hybrid"] = "class"
    forced_encapsulation: bool = True
    encapsulation_method: typing.Literal["disabled", "enforced", "hybrid"] = "enforced"

@dataclass(frozen=True, kw_only=True)
class InlineCommentCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["#", "//", ";", "--", "%"] = "#"
    space_required: bool = True

@dataclass(frozen=True, kw_only=True)
class MultilineCommentSyntaxConfigCls(CustomDataclass):
    start: typing.Literal["/*", "###", "#=",
                          "#*", "(*", "<!--",
                          "{#", "{{!--", "{{--",
                          "--[[", "#|", "%{"] = "/*"
    end: typing.Literal["*/", "###", "=#",
                        "*#", "--}}", "]]",
                        "|#", "}%"] = "*/"

@dataclass(frozen=True, kw_only=True)
class MultilineCommentConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: MultilineCommentSyntaxConfigCls = MultilineCommentSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class CommentConfigCls(CustomDataclass):
    inline_comment: InlineCommentCls = InlineCommentCls()
    multiline_comment: MultilineCommentConfigCls = MultilineCommentConfigCls()

@dataclass(frozen=True, kw_only=True)
class VariablesConfigCls(CustomDataclass):
    implicit_globals: bool = False
    function_hoisting: bool = True

@dataclass(frozen=True, kw_only=True)
class UncategorizedConfigCls(CustomDataclass):
    implicit_return: bool = False
    trailing_comma: typing.Literal["always", "never", "single_tuple_only"] = "always"
    semicolon_required: bool = False
    soft_keywords: bool = False
    code_blocks: typing.Literal["indentation", "braces", "end"] = "braces"
    mutable_value_assignment_behavior: typing.Literal["copy", "reference"] = "copy"

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