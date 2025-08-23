import typing
from dataclasses import dataclass, field

from backend.config.baseclasses import CustomDataclass, ConfigDescriptor, _UNFILLED

Accessibility: typing.TypeAlias = typing.Literal["never", "always",
                                                  "enable_by_prefix",
                                                  "enable_by_delimeter",
                                                  "disable_by_prefix",
                                                  "disable_by_delimeter"]
StringDelimeters: typing.TypeAlias = list[typing.Literal["'", '"', "`"]]


@dataclass(frozen=True, kw_only=True)
class NumericSeparatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["_", " "]] = ConfigDescriptor(_UNFILLED, "_")

@dataclass(frozen=True, kw_only=True)
class IntegerBaseLiteralsConfigCls(CustomDataclass):
    binary: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    decimal: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    octal: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    hexadecimal: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class NumberLiteralsConfigCls(CustomDataclass):
    numeric_separator: NumericSeparatorConfigCls = NumericSeparatorConfigCls()
    integer_base_literals: IntegerBaseLiteralsConfigCls = IntegerBaseLiteralsConfigCls()
    scientific_notation: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class BooleanSyntaxConfigCls(CustomDataclass):
    true: ConfigDescriptor[typing.Literal["true", "True", "TRUE", "yes", "Yes", "y", "Y", "Affirmative", "ye", "yup", "yay"]] = ConfigDescriptor(_UNFILLED, "true")
    false: ConfigDescriptor[typing.Literal["false", "False", "FALSE", "no", "No", "n", "N", "Negative", "nah", "nope", "nay"]] = ConfigDescriptor(_UNFILLED, "false")

@dataclass(frozen=True, kw_only=True)
class BooleanLiteralsConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    case_insensivity: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, False)
    syntax: BooleanSyntaxConfigCls = BooleanSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class NullLiteralConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    case_insensivity: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, False)
    syntax: ConfigDescriptor[typing.Literal["null", "Null", "NULL", "None", "none", "NOTHING", "nothing", "Nothing", "undefined", "nil"]] = ConfigDescriptor(_UNFILLED, "null")

@dataclass(frozen=True, kw_only=True)
class StrInterpolationExpressionSyntaxConfigCls(CustomDataclass):
    start: ConfigDescriptor[typing.Literal["{", "${", "#{", "%{", "\\{", "[", "$[", "#[", "%[", "\\[", "(", "$(", "#(", "%(", "\\("]] = ConfigDescriptor(_UNFILLED, "{")
    end: ConfigDescriptor[typing.Literal["]", "}", ")"]] = ConfigDescriptor(_UNFILLED, "}")

@dataclass(frozen=True, kw_only=True)
class StrInterpolationConfigCls(CustomDataclass):
    accessibility: ConfigDescriptor[Accessibility] = ConfigDescriptor(_UNFILLED, "enable_by_prefix")
    expression_syntax: StrInterpolationExpressionSyntaxConfigCls = StrInterpolationExpressionSyntaxConfigCls()
    allow_identifier_syntax: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, False)
    identifier_prefix_syntax: ConfigDescriptor[typing.Literal["$", "#", "\\", "%"]] = ConfigDescriptor(_UNFILLED, "$")
    force_escape_closing_bracket: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    delimeter_syntax: ConfigDescriptor[StringDelimeters] = ConfigDescriptor(_UNFILLED, ["'", "\"", "`"])
    prefix: ConfigDescriptor[typing.Literal["f", "i"]] = ConfigDescriptor(_UNFILLED, "f")

@dataclass(frozen=True, kw_only=True)
class MultilineStrConfigCls(CustomDataclass):
    acceessibility: ConfigDescriptor[Accessibility] = ConfigDescriptor(_UNFILLED, "enable_by_delimeter")
    delimeter_syntax: ConfigDescriptor[StringDelimeters | typing.Literal["triple"]] = ConfigDescriptor(_UNFILLED, "triple")

@dataclass(frozen=True, kw_only=True)
class StringLiteralsConfigCls(CustomDataclass):
    delimeters: StringDelimeters = field(default_factory = lambda: ["'", "`", '"'])
    interpolation: StrInterpolationConfigCls = StrInterpolationConfigCls()
    multiline: MultilineStrConfigCls = MultilineStrConfigCls()

@dataclass(frozen=True, kw_only=True)
class EllipsisLiteralConfigCls(CustomDataclass):
    pass

@dataclass(frozen=True, kw_only=True)
class LiteralsConfigCls(CustomDataclass):
    numbers: NumberLiteralsConfigCls = NumberLiteralsConfigCls()
    booleans: BooleanLiteralsConfigCls = BooleanLiteralsConfigCls()
    null: NullLiteralConfigCls = NullLiteralConfigCls()
    strings: StringLiteralsConfigCls = StringLiteralsConfigCls()
    ellipsis: EllipsisLiteralConfigCls = EllipsisLiteralConfigCls()