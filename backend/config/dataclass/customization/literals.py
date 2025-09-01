import itertools
import typing
from dataclasses import dataclass, field

from backend.config.baseclasses import CustomDataclass, ConfOptWrapper as C, _UNFILLED
from backend import errors

Accessibility: typing.TypeAlias = typing.Literal["never", "always",
                                                  "enable_by_prefix",
                                                  "enable_by_delimeter",
                                                  "disable_by_prefix",
                                                  "disable_by_delimeter"]
StringDelimeters: typing.TypeAlias = list[typing.Literal["'", '"', "`"]]


@dataclass(frozen=True, kw_only=True)
class NumericSeparatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(default = True)
    syntax: C[typing.Literal["_", " "]] = C(default = "_")

@dataclass(frozen=True, kw_only=True)
class IntegerBaseLiteralsConfigCls(CustomDataclass):
    binary: C[bool] = C(default = True)
    decimal: C[bool] = C(default = True)
    octal: C[bool] = C(default = True)
    hexadecimal: C[bool] = C(default = True)
    def validate_config(self):
        disabled_integers = not any(i.get() for i in (self.binary, self.decimal,
                                                      self.octal, self.hexadecimal))
        if disabled_integers and not self.get_root_config_cls().masochistic_mode.get():
            raise errors.ConfigError(
                "At least 1 of the integer bases should be enabled."
            )
        super().validate_config()

@dataclass(frozen=True, kw_only=True)
class NumberLiteralsConfigCls(CustomDataclass):
    numeric_separator: NumericSeparatorConfigCls = NumericSeparatorConfigCls()
    integer_base_literals: IntegerBaseLiteralsConfigCls = IntegerBaseLiteralsConfigCls()
    scientific_notation: C[bool] = C(default = True)

@dataclass(frozen=True, kw_only=True)
class BooleanSyntaxConfigCls(CustomDataclass):
    true: C[typing.Literal["true", "True", "TRUE", "yes", "Yes", "y", "Y", "Affirmative", "ye", "yup", "yay"]] = C(default = "true")
    false: C[typing.Literal["false", "False", "FALSE", "no", "No", "n", "N", "Negative", "nah", "nope", "nay"]] = C(default = "false")

@dataclass(frozen=True, kw_only=True)
class BooleanLiteralsConfigCls(CustomDataclass):
    enabled: C[bool] = C(default = True)
    case_insensivity: C[bool] = C(default = False)
    syntax: BooleanSyntaxConfigCls = BooleanSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class NullLiteralConfigCls(CustomDataclass):
    enabled: C[bool] = C(default = True)
    case_insensivity: C[bool] = C(default = False)
    syntax: C[typing.Literal["null", "Null", "NULL", "None", "none", "NOTHING", "nothing", "Nothing", "undefined", "nil"]] = C(default = "null")

@dataclass(frozen=True, kw_only=True)
class StringInterpolationExpressionSyntaxConfigDataClass[Start: str, End: str](CustomDataclass):
    start: C[Start] = C(default = "{")
    end: C[End] = C(default = "}")

# & 67 characters long identifier
StringInterpolationExpressionSyntaxConfigDataClassMatchingTypeAlias: typing.TypeAlias = (
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
    accessibility: C[Accessibility] = C(default = "enable_by_prefix")
    expression_syntax: StringInterpolationExpressionSyntaxConfigDataClassMatchingTypeAlias = StringInterpolationExpressionSyntaxConfigDataClass()
    allow_identifier_syntax: C[bool] = C(default = False)
    identifier_prefix_syntax: C[typing.Literal["$", "#", "\\", "%"]] = C(default = "$")
    force_escape_closing_bracket: C[bool] = C(default = True)
    delimeter_syntax: C[StringDelimeters] = C(default = ["'", "\"", "`"])
    prefix_syntax: C[typing.Literal["f", "i"]] = C(default = "f")

@dataclass(frozen=True, kw_only=True)
class MultilineStrConfigCls(CustomDataclass):
    accessibility: C[Accessibility] = C(default = "enable_by_delimeter")
    delimeter_syntax: C[StringDelimeters | typing.Literal["triple"]] = C(default = "triple")
    prefix_syntax: C[typing.Literal["m"]] = C(default = "m")

@dataclass(frozen=True, kw_only=True)
class RawStrConfigCls(CustomDataclass):
    accessibility: C[Accessibility] = C(default = "enable_by_delimeter")
    delimeter_syntax: C[StringDelimeters] = C(default = "triple")
    prefix_syntax: C[typing.Literal["r", "l"]] = C(default = "r")

@dataclass(frozen=True, kw_only=True)
class ByteStrConfigCls(CustomDataclass):
    accessibility: C[Accessibility] = C(default = "enable_by_delimeter")
    delimeter_syntax: C[StringDelimeters] = C(default = "triple")
    prefix_syntax: C[typing.Literal["b"]] = C(default = "b")

@dataclass(frozen=True, kw_only=True)
class StringLiteralsConfigCls(CustomDataclass):
    delimeters: StringDelimeters = field(default_factory = lambda: ["'", "`", '"'])
    interpolation: StrInterpolationConfigCls = StrInterpolationConfigCls()
    multiline: MultilineStrConfigCls = MultilineStrConfigCls()
    raw_string: RawStrConfigCls = RawStrConfigCls()
    byte_string: ByteStrConfigCls = ByteStrConfigCls()

    def validate_config(self):
        for category, name in self._():
            if category.accessibility.get().endswith(""):
                for quote in category.delimeter_syntax.get():
                    if quote not in self.delimeters:
                        raise errors.ConfigError(
                            "Any delimeters in the string's subcategories must be "
                            "present in the root delimeters config option as well.\n"
                            f"In particular: {quote} from category {name}."
                        )
        super().validate_config()

    def _(self):
        # TODO: Give this function a proper name
        yield self.interpolation, "interpolation"
        yield self.multiline, "multiline"
        yield self.raw_string, "raw_string"
        yield self.byte_string, "byte_string"

    def get_all_possible_starts(self) -> list[str]:
        ls = []
        prefixes = []
        for category, _ in self._():
            if category.accessibility.endswith("prefix"):
                prefixes.append(category.prefix_syntax.get())
        for n in range(len(prefixes) + 1):
            for perm in itertools.permutations(prefixes, n):
                ls.extend(
                    "".join(perm)+quote for quote in self.delimeters
                )
        return ls

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