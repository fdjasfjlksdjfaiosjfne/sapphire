from __future__ import annotations
import keyword
import typing
import regex
from dataclasses import dataclass, fields, is_dataclass


from backend import errors
from backend.config.checks import asserting_config_dict
from backend.config.baseclasses import CustomDataclass, ConfigDescriptor, _UNFILLED

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
    ClassicConditionalConfigCls,
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
    ClassicConditionalSyntaxConfigCls,
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

def convert_name(name: str) -> str:
    snake_case_name = camel_to_snake(name)
    if keyword.iskeyword(name) or keyword.issoftkeyword(name):
        snake_case_name += "_"
    return snake_case_name

ForcableTemplate: typing.TypeAlias = typing.Literal["disabled", "enabled", "forced"]
UnforcableTemplate: typing.TypeAlias = typing.Literal["disabled", "enabled"]

FIELD_ALIASES = {
    "customization": ["customization", "customisation"],
    "mutable_value_assignment_behavior": ["mutable_value_assignment_behavior", "mutable_value_assignment_behaviour"],
    "mutable_value_as_default_behavior": ["mutable_value_as_default_behavior", "mutable_value_as_default_behaviour"],
    "typeBehavior": ["typeBehavior", "typeBehaviour"]
}

@dataclass(frozen=True, kw_only=True)
class ConfigVersionCls(CustomDataclass):
    major: ConfigDescriptor[int] = ConfigDescriptor(_UNFILLED, 2)
    minor: ConfigDescriptor[int] = ConfigDescriptor(_UNFILLED, 1)
    patch: ConfigDescriptor[int] = ConfigDescriptor(_UNFILLED, 1)
    phase: ConfigDescriptor[
           typing.Literal["indev", "alpha",
                          "beta", "release"]] = "indev" # type: ignore
    def __repr__(self) -> str:
        return (
            f"<ConfigVersionCls: {self.major}.{self.minor}.{self.patch}"
            f"; phase {self.phase}>"
        )

@dataclass(frozen=True, kw_only=True)
class TemplatesCls(CustomDataclass):
    inverted_comparisons: ConfigDescriptor[ForcableTemplate] = "disabled" # type: ignore
    methify: ConfigDescriptor[ForcableTemplate] = "disabled" # type: ignore
    def __init__(self, **kwargs):
        for k, v in list(kwargs.items()):
            match v:
                case 1 | "enabled" | True:
                    kwargs[k] = "enabled"
                case 2 | "forced":
                    kwargs[k] = "forced"
                case 0 | "disabled" | False:
                    kwargs[k] = "disabled"
        super().__init__(**kwargs)


@dataclass(frozen=True, kw_only=True)
class RootConfigCls(CustomDataclass):
    """The very root of the configuration dataclass object.

    This field itself contains five attributes:
    - `customization`: Has most of the options you're looking for.
    - `templates`: A list of optional, fixed modifications.
    - `config_version`: Self-explanatory.
    - `advanced_mode`: Locks behind options that may not be beginner-friendly
    - `masochistic_mode`: Locks behind options that would otherwise make DX miserable

    Note that every attribute (including subcategories btw) is 
    actually a descriptor. The static type checker may say 
    otherwise, but they...they are all descriptors, trust me pls :<

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
    - `is_default()`: The opposite of the aforementioned.
    """
    customization: CustomizationConfigCls = CustomizationConfigCls()
    templates: TemplatesCls = TemplatesCls()
    config_version: ConfigVersionCls = ConfigVersionCls()
    advanced_mode: ConfigDescriptor[bool] = ConfigDescriptor(default = False)
    masochistic_mode: ConfigDescriptor[bool] = ConfigDescriptor(default = False)

    @classmethod
    def from_dict(cls, config_dict: dict[str, typing.Any]) -> RootConfigCls:
        """
        Factory method that handles pre-processing of config dictionaries.
        """
        normalized_dict = cls._normalize_dict(config_dict)
        asserting_config_dict(config_dict)
        return typing.cast(
            RootConfigCls,
            RootConfigCls._solidify_config_dict(RootConfigCls, config_dict)
        )
    
    @staticmethod
    def _normalize_dict(data: dict[str, typing.Any]) -> dict[str, typing.Any]:
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