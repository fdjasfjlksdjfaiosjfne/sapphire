

import typing
from dataclasses import dataclass, field

from backend.config.baseclasses import CustomDataclass

Accessibility: typing.TypeAlias = typing.Literal["never", "always",
                                                  "enable_by_prefix",
                                                  "enable_by_delimeter",
                                                  "disable_by_prefix",
                                                  "disable_by_delimeter"]
StringDelimeters: typing.TypeAlias = list[typing.Literal["'", '"', "`"]]


@dataclass(frozen=True, kw_only=True)
class NumericSeparatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["_", " "] = "_"

@dataclass(frozen=True, kw_only=True)
class IntegerBaseLiteralsConfigCls(CustomDataclass):
    binary: bool = True
    decimal: bool = True
    octal: bool = True
    hexadecimal: bool = True

@dataclass(frozen=True, kw_only=True)
class NumberLiteralsConfigCls(CustomDataclass):
    numeric_separator: NumericSeparatorConfigCls = NumericSeparatorConfigCls()
    integer_base_literals: IntegerBaseLiteralsConfigCls = IntegerBaseLiteralsConfigCls()
    scientific_notation: bool = True

@dataclass(frozen=True, kw_only=True)
class BooleanSyntaxConfigCls(CustomDataclass):
    true: typing.Literal["true", "True", "TRUE", "yes", "Yes", "y", "Y", "Affirmative", "ye", "yup", "yay"] = "true"
    false: typing.Literal["false", "False", "FALSE", "no", "No", "n", "N", "Negative", "nah", "nope", "nay"] = "false"

@dataclass(frozen=True, kw_only=True)
class BooleanLiteralsConfigCls(CustomDataclass):
    enabled: bool = True
    case_insensivity: bool = False
    syntax: BooleanSyntaxConfigCls = BooleanSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class NullLiteralConfigCls(CustomDataclass):
    enabled: bool = True
    case_insensivity: bool = False
    syntax: typing.Literal["null", "Null", "NULL", "None", "none", "NOTHING", "nothing", "Nothing", "undefined", "nil"] = "null"

@dataclass(frozen=True, kw_only=True)
class StrInterpolationExpressionSyntaxConfigCls(CustomDataclass):
    start: typing.Literal["{", "${", "#{", "%{", "\\{",
                          "[", "$[", "#[", "%[", "\\[",
                          "(", "$(", "#(", "%(", "\\("] = "{"
    end: typing.Literal["]", "}", ")"] = "}"


@dataclass(frozen=True, kw_only=True)
class StrInterpolationConfigCls(CustomDataclass):
    accessibility: Accessibility = "enable_by_prefix"
    expression_syntax: StrInterpolationExpressionSyntaxConfigCls = StrInterpolationExpressionSyntaxConfigCls()
    allow_identifier_syntax: bool = False
    identifier_prefix_syntax: typing.Literal["$", "#", "\\", "%"] = "$"
    force_escape_closing_bracket: bool = True
    delimeter_syntax: StringDelimeters = None # type: ignore
    prefix: typing.Literal["f", "i"] = "f"
    def __post_init__(self):
        if self.delimeter_syntax is None:
            object.__setattr__(self, "delimeter_syntax", ["'", "\"", "`"])

@dataclass(frozen=True, kw_only=True)
class MultilineStrConfigCls(CustomDataclass):
    acceessibility: Accessibility = "enable_by_delimeter"
    delimeter_syntax: StringDelimeters | typing.Literal["triple"] = "triple"


@dataclass(frozen=True, kw_only=True)
class StringLiteralsConfigCls(CustomDataclass):
    delimeters: StringDelimeters = None # type: ignore
    interpolation: StrInterpolationConfigCls = StrInterpolationConfigCls()
    multiline: MultilineStrConfigCls = MultilineStrConfigCls()
    def __post_init__(self):
        if self.delimeters is None:
            object.__setattr__(self, "delimeters", ["\"", "'", "`"])

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