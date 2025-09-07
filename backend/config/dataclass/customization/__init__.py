import typing
from dataclasses import dataclass

from backend.config.dataclass.bases import CustomConfDatacls, ConfOptWrapper, _UNFILLED
from backend.config.dataclass.customization.literals import *
from backend.config.dataclass.customization.control import *
from backend.config.dataclass.customization.objects import *
from backend.config.dataclass.customization.operators import *

@dataclass(frozen=True, kw_only=True)
class AnnotationsConfigCls(CustomConfDatacls):
    enabled: C[bool] = C(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class OOPConfigCls(CustomConfDatacls):
    oop_model: C[typing.Literal["class", "prototype", "hybrid"]] = C(_UNFILLED, "class")
    forced_encapsulation: C[bool] = C(_UNFILLED, True)
    encapsulation_method: C[typing.Literal["disabled", "enforced", "hybrid"]] = C(_UNFILLED, "enforced")

@dataclass(frozen=True, kw_only=True)
class InlineCommentCls(CustomConfDatacls):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["#", "//", ";", "--", "%", "::"]] = C(_UNFILLED, "#")
    space_required: C[bool] = C(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class MultilineCommentSyntaxConfigCls[Start: str, End: str](CustomConfDatacls):
    start: C[Start] = C(default = "/*")
    end: C[End] = C(default = "*/")

MultiLineCommentSyntax: typing.TypeAlias = (
      MultilineCommentSyntaxConfigCls[typing.Literal["/*"], typing.Literal["*/"]]
    | MultilineCommentSyntaxConfigCls[typing.Literal["#" "#" "#"], typing.Literal["#" "#" "#"]]
    | MultilineCommentSyntaxConfigCls[typing.Literal["#="], typing.Literal["=#"]]
    | MultilineCommentSyntaxConfigCls[typing.Literal["#" "*" # > See docs/conventions.md#Technical_Limitations
                                                            ], typing.Literal["*#"]]
    | MultilineCommentSyntaxConfigCls[typing.Literal["(*)"], typing.Literal["*)"]]
    | MultilineCommentSyntaxConfigCls[typing.Literal["<!--"], typing.Literal["-->"]]
    | MultilineCommentSyntaxConfigCls[typing.Literal["{#"], typing.Literal["#}"]]
    | MultilineCommentSyntaxConfigCls[typing.Literal["{{--"], typing.Literal["--}}"]]
    | MultilineCommentSyntaxConfigCls[typing.Literal["{{!--"], typing.Literal["--}}"]]
    | MultilineCommentSyntaxConfigCls[typing.Literal["--[["], typing.Literal["]]"]]
    | MultilineCommentSyntaxConfigCls[typing.Literal["#|"], typing.Literal["|#"]]
    | MultilineCommentSyntaxConfigCls[typing.Literal["%{"], typing.Literal["}%"]]
)

@dataclass(frozen=True, kw_only=True)
class MultilineCommentConfigCls(CustomConfDatacls):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: MultilineCommentSyntaxConfigCls = MultilineCommentSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class CommentConfigCls(CustomConfDatacls):
    inline_comment: InlineCommentCls = InlineCommentCls()
    multiline_comment: MultilineCommentConfigCls = MultilineCommentConfigCls()

@dataclass(frozen=True, kw_only=True)
class VariablesConfigCls(CustomConfDatacls):
    implicit_globals: C[bool] = C(_UNFILLED, False)
    function_hoisting: C[bool] = C(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class UncategorizedConfigCls(CustomConfDatacls):
    implicit_return: C[bool] = C(_UNFILLED, False)
    trailing_comma: C[typing.Literal["always", "never", "single_tuple_only"]] = C(_UNFILLED, "always")
    semicolon_required: C[bool] = C(_UNFILLED, False)
    soft_keywords: C[bool] = C(_UNFILLED, False)
    code_blocks: C[typing.Literal["indentation", "braces", "end"]] = C(_UNFILLED, "braces")
    mutable_value_assignment_behavior: C[typing.Literal["copy", "reference"]] = C(_UNFILLED, "copy")

@dataclass(frozen=True, kw_only=True)
class CustomizationConfigCls(CustomConfDatacls):
    """The configuration class, which contains most the options you might be looking for.

    This has 9 subcategories:
    - `annotations`: Controls type annotations.
    - `literals`: Controls literal types, like strings, numbers, booleans, etc.
    - `comments`: Controls comments.
    - `control_flow`: Controls various control statements, like conditional statements.
    - `variables`: Controls variables.
    - `objects`: Controls non-literal types, like functions, classes, arrays, etc.
    - `oop`: Controls the object-orientation aspect.
    - `operators`: Controls operators.
    - `uncategorized`: Contains various unrelated settings that don't fit in the other categories.
    """
    annotations: AnnotationsConfigCls = AnnotationsConfigCls()
    literals: LiteralsConfigCls = LiteralsConfigCls()
    comments: CommentConfigCls = CommentConfigCls()
    control_flow: ControlFlowConfigCls = ControlFlowConfigCls()
    variables: VariablesConfigCls = VariablesConfigCls()
    objects: ObjectsConfigCls = ObjectsConfigCls()
    oop: OOPConfigCls = OOPConfigCls()
    operators: OperatorsConfigCls = OperatorsConfigCls()
    uncategorized: UncategorizedConfigCls = UncategorizedConfigCls()