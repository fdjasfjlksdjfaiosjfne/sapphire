import typing
from dataclasses import dataclass, fields

from backend.config.baseclasses import custom_dataclass

from backend.config.dataclass.customization import (
    CustomizationConfigCls,
    LiteralsConfigCls,
    NumberLiteralsConfigCls,
    NumericSeparatorConfigCls,
    IntegerBaseLiteralsConfigCls,
    BooleanLiteralsConfigCls,
    BooleanSyntaxConfigCls,
    NullLiteralConfigCls,
    EllipsisLiteralConfigCls,
    StringLiteralsConfigCls,
    StrInterpolationConfigCls,
    StrInterpolationExpressionSyntaxConfigCls,
    MultilineStrConfigCls,
    ControlFlowConfigCls,
    ConditionalConfigCls,
    CommentConfigCls,
    EnumsConfigCls,
    ClassesConfigCls,
    JumpingConfigCls,
    ObjectsConfigCls,
    ConditionalSyntaxConfigCls,
    ComparisonOperatorsConfigCls,
    FunctionsConfigCls,
    MatchCaseConfigCls,
    OperatorsConfigCls,
    VariablesConfigCls,
    ThrowErrorConfigCls,
    AnnotationsConfigCls,
    FnArgumentsConfigCls,
    TryStatementConfigCls,
    UncategorizedConfigCls,
    OtherOperatorsConfigCls,
    BinaryOperatorsConfigCls,
    StringConcanentationConfigCls,
    InlineCommentCls,
    ModulusOperatorConfigCls,
    AdditionOperatorConfigCls,
    BooleanOperatorsConfigCls,
    EqualityOperatorConfigCls,
    LogicalOperatorsConfigCls,
    MultilineCommentConfigCls,
    BinaryAndOperatorConfigCls,
    ExceptionHandlingConfigCls,
    NoExceptionClauseConfigCls,
    BooleanAndOperatorConfigCls,
    FinalCleanupClauseConfigCls,
    InequalityOperatorConfigCls,
    LogicalAndOperatorConfigCls,
    ArithmeticOperatorsConfigCls,
    SubtractionOperatorConfigCls,
    MatrixMultiplicationConfigCls,
    TrueDivisionOperatorConfigCls,
    ExponentationOperatorConfigCls,
    FloorDivisionOperatorConfigCls,
    LooseEqualityOperatorsConfigCls,
    MultilineCommentSyntaxConfigCls,
    MultiplicationOperatorConfigCls,
    ExceptionHandlingClauseConfigCls,
    BinaryExclusiveOrOperatorConfigCls,
    BinaryInclusiveOrOperatorConfigCls,
    BooleanExclusiveOrOperatorConfigCls,
    BooleanInclusiveOrOperatorConfigCls,
    LogicalExclusiveOrOperatorConfigCls,
    LogicalInclusiveOrOperatorConfigCls
)

ForcableTemplate: typing.TypeAlias = typing.Literal["disabled", "enabled", "forced"]
UnforcableTemplate: typing.TypeAlias = typing.Literal["disabled", "enabled"]

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ConfigVersionCls:
    major: int = 2
    minor: int = 1
    patch: int = 0
    phase: typing.Literal["indev", "alpha",
                          "beta", "release"] = "indev"
    def __repr__(self) -> str:
        return (
            f"<ConfigVersionCls: {self.major}.{self.minor}.{self.patch}"
            f"; phase {self.phase}>"
        )

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class TemplatesCls:
    inverted_comparisons: ForcableTemplate = "disabled"
    methify: ForcableTemplate = "disabled"
    def __post_init__(self):
        for field in fields(self):
            match getattr(self, field.name).get_value():
                case 0 | False:
                    object.__setattr__(self, field.name, "disabled")
                case 1 | True:
                    object.__setattr__(self, field.name, "enabled")
                case 2:
                    object.__setattr__(self, field.name, "forced")

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class RootConfigCls:
    """The very root of the configuration object.

    This field contains three attributes:
    - `customization`: Has most of the options you're looking for.
    - `templates`: A list of optional, fixed modifications.
    - `config_version`: Self-explanatory.

    Note that every attribute (including subcategories btw) is 
    actually a descriptor. The static type checker may say 
    otherwise, but they...they are all descriptors, trust me :<

    Here's a list of the descriptor methods:
    - `__get__()` (aka. just don't call anything): For most 
    purposes, this will probably be the method you're looking 
    for.
    - `get_value(*, return_unfilled: bool = False)`: Since the 
    `match`/`case` statement doesn't play nice with descriptors...
    this aims to fix that by returning the pure value. The 
    keyword-only `return_unfilled` argument determines whether 
    the method will return the default value if the value is the 
    `_UNFILLED` sentinel object.
    - `is_explicit()`: Returns `True` if the value is explicitly
    filled (i.e. not `_UNFILLED`)
    - `is_default()`: It's `not is_explicit()`.
    - `__set__()`, `__del__()` and `__delete__()`: Just throw an error.
    Don't bother.
    """
    customization: CustomizationConfigCls = CustomizationConfigCls()
    templates: TemplatesCls = TemplatesCls()
    config_version: ConfigVersionCls = ConfigVersionCls()