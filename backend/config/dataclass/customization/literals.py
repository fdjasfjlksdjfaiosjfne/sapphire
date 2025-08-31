import typing
from dataclasses import dataclass, field

from backend.config.baseclasses import CustomDataclass, ConfigDescriptor as C, _UNFILLED

Accessibility: typing.TypeAlias = typing.Literal["never", "always",
                                                  "enable_by_prefix",
                                                  "enable_by_delimeter",
                                                  "disable_by_prefix",
                                                  "disable_by_delimeter"]
StringDelimeters: typing.TypeAlias = list[typing.Literal["'", '"', "`"]]


@dataclass(frozen=True, kw_only=True)
class NumericSeparatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["_", " "]] = C(_UNFILLED, "_")

@dataclass(frozen=True, kw_only=True)
class IntegerBaseLiteralsConfigCls(CustomDataclass):
    binary: C[bool] = C(_UNFILLED, True)
    decimal: C[bool] = C(_UNFILLED, True)
    octal: C[bool] = C(_UNFILLED, True)
    hexadecimal: C[bool] = C(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class NumberLiteralsConfigCls(CustomDataclass):
    numeric_separator: NumericSeparatorConfigCls = NumericSeparatorConfigCls()
    integer_base_literals: IntegerBaseLiteralsConfigCls = IntegerBaseLiteralsConfigCls()
    scientific_notation: C[bool] = C(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class BooleanSyntaxConfigCls(CustomDataclass):
    true: C[typing.Literal["true", "True", "TRUE", "yes", "Yes", "y", "Y", "Affirmative", "ye", "yup", "yay"]] = C(_UNFILLED, "true")
    false: C[typing.Literal["false", "False", "FALSE", "no", "No", "n", "N", "Negative", "nah", "nope", "nay"]] = C(_UNFILLED, "false")

@dataclass(frozen=True, kw_only=True)
class BooleanLiteralsConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    case_insensivity: C[bool] = C(_UNFILLED, False)
    syntax: BooleanSyntaxConfigCls = BooleanSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class NullLiteralConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    case_insensivity: C[bool] = C(_UNFILLED, False)
    syntax: C[typing.Literal["null", "Null", "NULL", "None", "none", "NOTHING", "nothing", "Nothing", "undefined", "nil"]] = C(_UNFILLED, "null")

@dataclass(frozen=True, kw_only=True)
class StringInterpolationExpressionSyntaxConfigDataClass[Start: str, End: str](CustomDataclass):
    start: C[Start] = C(default = "{")
    end: C[End] = C(default = "}")

# & 68 characters long
StringInterpolationExpresssionSyntaxConfigDataClassMatchingTypeAlias: typing.TypeAlias = (
      StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal[ "{" ], typing.Literal["}"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["${" ], typing.Literal["}"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["#{" ], typing.Literal["}"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["%{" ], typing.Literal["}"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["\\{"], typing.Literal["}"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal[ "[" ], typing.Literal["]"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["$[" ], typing.Literal["]"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["#[" ], typing.Literal["]"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["%[" ], typing.Literal["]"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["\\["], typing.Literal["]"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal[ "(" ], typing.Literal[")"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["$(" ], typing.Literal[")"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["#(" ], typing.Literal[")"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["%(" ], typing.Literal[")"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["\\("], typing.Literal[")"]]
)

@dataclass(frozen=True, kw_only=True)
class StrInterpolationConfigCls(CustomDataclass):
    accessibility: C[Accessibility] = C(_UNFILLED, "enable_by_prefix")
    expression_syntax: StringInterpolationExpresssionSyntaxConfigDataClassMatchingTypeAlias = StringInterpolationExpressionSyntaxConfigDataClass()
    allow_identifier_syntax: C[bool] = C(_UNFILLED, False)
    identifier_prefix_syntax: C[typing.Literal["$", "#", "\\", "%"]] = C(_UNFILLED, "$")
    force_escape_closing_bracket: C[bool] = C(_UNFILLED, True)
    delimeter_syntax: C[StringDelimeters] = C(_UNFILLED, ["'", "\"", "`"])
    prefix: C[typing.Literal["f", "i"]] = C(_UNFILLED, "f")

@dataclass(frozen=True, kw_only=True)
class MultilineStrConfigCls(CustomDataclass):
    accessibility: C[Accessibility] = C(_UNFILLED, "enable_by_delimeter")
    delimeter_syntax: C[StringDelimeters | typing.Literal["triple"]] = C(_UNFILLED, "triple")
    prefix_syntax: C[typing.Literal["m"]] = C(_UNFILLED, "m")

@dataclass(frozen=True, kw_only=True)
class RawStrConfigCls(CustomDataclass):
    accessibility: C[Accessibility] = C(_UNFILLED, "enable_by_delimeter")
    delimeter_syntax: C[StringDelimeters | typing.Literal["triple"]] = C(_UNFILLED, "triple")
    prefix_syntax: C[typing.Literal["r", "l"]] = C(_UNFILLED, "r")

@dataclass(frozen=True, kw_only=True)
class StringLiteralsConfigCls(CustomDataclass):
    delimeters: StringDelimeters = field(default_factory = lambda: ["'", "`", '"'])
    interpolation: StrInterpolationConfigCls = StrInterpolationConfigCls()
    multiline: MultilineStrConfigCls = MultilineStrConfigCls()
    raw_string: RawStrConfigCls = RawStrConfigCls()

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