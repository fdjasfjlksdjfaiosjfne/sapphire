from __future__ import annotations
import typing
import regex
from dataclasses import dataclass, fields, is_dataclass


from backend import errors
from backend.config.checks import asserting_config_dict
from backend.config.baseclasses import CustomDataclass

from backend.config.dataclass.customization import (
    CustomizationConfigCls,
    EnumsConfigCls,
    ClassesConfigCls,
    JumpingConfigCls,
    ObjectsConfigCls,
    InlineCommentCls,
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
    ModulusOperatorConfigCls,
    AdditionOperatorConfigCls,
    BooleanOperatorsConfigCls,
    EqualityOperatorConfigCls,
    LogicalOperatorsConfigCls,
    MultilineCommentConfigCls,
    ConditionalSyntaxConfigCls,
    BinaryAndOperatorConfigCls,
    ExceptionHandlingConfigCls,
    NoExceptionClauseConfigCls,
    BooleanAndOperatorConfigCls,
    FinalCleanupClauseConfigCls,
    InequalityOperatorConfigCls,
    LogicalAndOperatorConfigCls,
    ArithmeticOperatorsConfigCls,
    SubtractionOperatorConfigCls,
    ComparisonOperatorsConfigCls,
    StringConcanentationConfigCls,
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

CAMEL_TO_SNAKE_PATTERN = regex.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

def camel_to_snake(string: str) -> str:
    return CAMEL_TO_SNAKE_PATTERN.sub(r"_\1", string).lower()

ForcableTemplate: typing.TypeAlias = typing.Literal["disabled", "enabled", "forced"]
UnforcableTemplate: typing.TypeAlias = typing.Literal["disabled", "enabled"]

FIELD_ALIASES = {
    "customization": ["customization", "customisation"],
    "mutable_value_assignment_behavior": ["mutable_value_assignment_behavior", "mutable_value_assignment_behaviour"],
    "mutable_value_as_default_behavior": ["mutable_Value_as_default_behavior", "mutable_value_as_default_behaviour"]
}

@dataclass(frozen=True, kw_only=True)
class ConfigVersionCls(CustomDataclass):
    major: int = 2
    minor: int = 1
    patch: int = 1
    phase: typing.Literal["indev", "alpha",
                          "beta", "release"] = "indev"
    def __repr__(self) -> str:
        return (
            f"<ConfigVersionCls: {self.major}.{self.minor}.{self.patch}"
            f"; phase {self.phase}>"
        )

@dataclass(frozen=True, kw_only=True)
class TemplatesCls(CustomDataclass):
    inverted_comparisons: ForcableTemplate = "disabled"
    methify: ForcableTemplate = "disabled"
    def __init__(self, **kwargs):
        for k, v in list(kwargs.items()):
            match v:
                case 1 | "enabled" | True:
                    kwargs[k] = "enabled"
                case 2 | "forced":
                    kwargs[k] = "forced"
                case 0 | "disabled" | False:
                    kwargs[k] = "disabled"
                case _:
                    raise errors.InternalError(
                        f"Invalid value in {k}: {v}"
                    )
        super().__init__(**kwargs)


@dataclass(frozen=True, kw_only=True)
class RootConfigCls(CustomDataclass):
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

    @classmethod
    def from_dict(cls, config_dict: dict[str, typing.Any]) -> RootConfigCls:
        """
        Factory method that handles pre-processing of config dictionaries.
        """
        normalized_dict = cls._normalize_aliases(config_dict)
        asserting_config_dict(config_dict)
        return typing.cast(
            RootConfigCls,
            RootConfigCls._solidify_config_dict(RootConfigCls, config_dict)
        )
    
    @staticmethod
    def _normalize_aliases(data: dict[str, typing.Any]) -> dict[str, typing.Any]:
        alias_to_canonical = {}
        for canonical, alias_list in FIELD_ALIASES.items():
            alias_to_canonical.update(
                {alias: canonical for alias in alias_list if alias != canonical}
            )
        
        def recursive(d):
            if not isinstance(d, dict):
                return d
            
            normalized = {}
            for key, value in d.items():
                key = camel_to_snake(key)
                canonical_key = alias_to_canonical.get(key, key)
                normalized[canonical_key] = recursive(value)
            return normalized

        return recursive(data)
    
    @staticmethod
    def _solidify_config_dict[T1, T2: dict](cls_: type[T1], data: T2) -> T1 | T2:
        """
        Recursively build dataclass instances from nested dictionaries.
        Automatically handles nested dataclasses and missing keys.
        """
        if not is_dataclass(cls_):
            return data
        
        kwargs = {}
        type_hints = typing.get_type_hints(cls_)

        for field in fields(cls_):
            field_name = field.name
            field_type = type_hints.get(field_name, field.type)
            field_value = None
            found_keys = []

            possible_names = FIELD_ALIASES.get(field_name, [field_name])
            for possible_name in possible_names:
                if possible_name in data:
                    found_keys.append(possible_name)
                    field_value = data[possible_name]
            
            if len(found_keys) > 1:
                raise errors.ConfigError(
                    f"Multiple spellings found for field '{field_name}': {found_keys}. "
                    f"Use only one of: {possible_names}"
                )
            
            if field_value is not None:
                if hasattr(field_type, "__dataclass_fields__"):
                    kwargs[field_name] = RootConfigCls._solidify_config_dict(field_type, field_value)
                else:
                    kwargs[field_name] = field_value
        
        return cls_(**kwargs)