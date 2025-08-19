

import typing
from dataclasses import dataclass, field

from backend.config.baseclasses import custom_dataclass

Acceessibility: typing.TypeAlias = typing.Literal["never", "always",
                                                  "enable_by_prefix",
                                                  "enable_by_delimeter",
                                                  "disable_by_prefix",
                                                  "disable_by_delimeter"]
StringDelimeters: typing.TypeAlias = list[typing.Literal["'", '"', "`"]]

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class NumericSeparatorConfigCls:
    enabled: bool = True 
    syntax: typing.Literal["_", " "] = "_"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class IntegerBaseLiteralsConfigCls:
    binary: bool = True
    decimal: bool = True
    octal: bool = True
    hexadecimal: bool = True

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class NumberLiteralsConfigCls:
    numeric_separator: NumericSeparatorConfigCls = NumericSeparatorConfigCls()
    integer_base_literals = IntegerBaseLiteralsConfigCls()
    scientific_notation: bool = True

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class BooleanSyntaxConfigCls:
    true: typing.Literal["true", "True", "TRUE", "yes", "Yes", "y", "Y", "Affirmative", "ye", "yup", "yay"] = "true"
    false: typing.Literal["false", "False", "FALSE", "no", "No", "n", "N", "Negative", "nah", "nope", "nay"] = "false"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class BooleanLiteralsConfigCls:
    enabled: bool = True
    case_insensivity: bool = False
    syntax: BooleanSyntaxConfigCls = BooleanSyntaxConfigCls()
@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class NullLiteralConfigCls:
    enabled: bool = True
    case_insensivity: bool = False
    syntax: typing.Literal["null", "Null", "NULL", "None", "none", "NOTHING", "nothing", "Nothing", "undefined", "nil"] = "null"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class StrInterpolationExpressionSyntaxConfigCls:
    start: typing.Literal["{", "${", "#{", "%{", "\\{",
                          "[", "$[", "#[", "%[", "\\[",
                          "(", "$(", "#(", "%(", "\\("] = "{"
    end: typing.Literal["]", "}", ")"] = "}"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class StrInterpolationConfigCls:
    accessibility: Acceessibility = "enable_by_prefix"
    expression_syntax: StrInterpolationExpressionSyntaxConfigCls = StrInterpolationExpressionSyntaxConfigCls()
    allow_identifier_syntax: bool = False
    identifier_prefix_syntax: typing.Literal["$", "#", "\\", "%"] = "$"
    force_escape_closing_bracket: bool = True
    delimeter_syntax: StringDelimeters = ["'", "\"", "`"]
    prefix: typing.Literal["f", "i"] = "f"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class MultilineStrConfigCls:
    acceessibility: Acceessibility = "enable_by_delimeter"
    delimeter_syntax: StringDelimeters | typing.Literal["triple"] = "triple"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class StringLiteralsConfigCls:
    delimeters: StringDelimeters = ["\"", "'", "`"]
    interpolation: StrInterpolationConfigCls = StrInterpolationConfigCls()
    multiline: MultilineStrConfigCls = MultilineStrConfigCls()

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class EllipsisLiteralConfigCls:
    pass

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class LiteralsConfigCls:
    numbers: NumberLiteralsConfigCls = NumberLiteralsConfigCls()
    booleans: BooleanLiteralsConfigCls = BooleanLiteralsConfigCls()
    null: NullLiteralConfigCls = NullLiteralConfigCls()
    strings: StringLiteralsConfigCls = StringLiteralsConfigCls()
    ellipsis: EllipsisLiteralConfigCls = EllipsisLiteralConfigCls()