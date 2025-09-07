from __future__ import annotations

import itertools
import typing
from dataclasses import dataclass

from backend.config.dataclass.bases import CustomConfDatacls, ConfOptWrapper as C
from backend import errors

if typing.TYPE_CHECKING:
    from backend.config.dataclass import CustomizationConfigCls

Accessibility: typing.TypeAlias = typing.Literal["never", "always",
                                                  "enable_by_prefix",
                                                  "enable_by_delimeter",
                                                  "disable_by_prefix",
                                                  "disable_by_delimeter"]
StringDelimeters: typing.TypeAlias = tuple[typing.Literal["'", '"', "`"]]


@dataclass(frozen=True, kw_only=True)
class NumericSeparatorConfigCls(CustomConfDatacls):
    enabled: C[bool] = C(default = True)
    syntax: C[typing.Literal["_", " "]] = C(default = "_")

@dataclass(frozen=True, kw_only=True)
class IntegerBaseLiteralsConfigCls(CustomConfDatacls):
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
class NumberLiteralsConfigCls(CustomConfDatacls):
    numeric_separator: NumericSeparatorConfigCls = NumericSeparatorConfigCls()
    integer_base_literals: IntegerBaseLiteralsConfigCls = IntegerBaseLiteralsConfigCls()
    scientific_notation: C[bool] = C(default = True)

@dataclass(frozen=True, kw_only=True)
class BooleanSyntaxConfigCls(CustomConfDatacls):
    true: C[typing.Literal["true", "True", "TRUE", "yes", "Yes", "y", "Y", "Affirmative", "ye", "yup", "yay"]] = C(default = "true")
    false: C[typing.Literal["false", "False", "FALSE", "no", "No", "n", "N", "Negative", "nah", "nope", "nay"]] = C(default = "false")

@dataclass(frozen=True, kw_only=True)
class BooleanLiteralsConfigCls(CustomConfDatacls):
    enabled: C[bool] = C(default = True)
    case_insensivity: C[bool] = C(default = False)
    syntax: BooleanSyntaxConfigCls = BooleanSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class NullLiteralConfigCls(CustomConfDatacls):
    enabled: C[bool] = C(default = True)
    case_insensivity: C[bool] = C(default = False)
    syntax: C[typing.Literal["null", "Null", "NULL", "None", "none", "NOTHING", "nothing", "Nothing", "undefined", "nil"]] = C(default = "null")

@dataclass(frozen=True, kw_only=True)
class StringInterpolationExpressionSyntaxConfigDataClass[Start: str, End: str](CustomConfDatacls):
    start: C[Start] = C(default = "{")
    end: C[End] = C(default = "}")

# & 70 characters long identifier
StringInterpolationExpressionSyntaxConfigDataClassCombinationTypeAlias: typing.TypeAlias = (
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
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal[ "<" ], typing.Literal[">"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["$<" ], typing.Literal[">"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["#<" ], typing.Literal[">"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["%<" ], typing.Literal[">"]]
    | StringInterpolationExpressionSyntaxConfigDataClass[typing.Literal["\\<"], typing.Literal[">"]]
)

@dataclass(frozen=True, kw_only=True)
class StrInterpolationConfigCls(CustomConfDatacls):
    accessibility: C[Accessibility] = C(default = "enable_by_prefix")
    expression_syntax: StringInterpolationExpressionSyntaxConfigDataClassCombinationTypeAlias = StringInterpolationExpressionSyntaxConfigDataClass()
    allow_identifier_syntax: C[bool] = C(default = False)
    identifier_prefix_syntax: C[typing.Literal["$", "#", "\\", "%"]] = C(default = "$")
    force_escape_closing_bracket: C[bool] = C(default = True)
    delimeter_syntax: C[StringDelimeters] = C(default = ["'", "\"", "`"])
    prefix_syntax: C[typing.Literal["f", "i", "$"]] = C(default = "f")

@dataclass(frozen=True, kw_only=True)
class MultilineStrConfigCls(CustomConfDatacls):
    accessibility: C[Accessibility] = C(default = "enable_by_delimeter")
    delimeter_syntax: C[StringDelimeters | typing.Literal["triple"]] = C(default = "triple")
    prefix_syntax: C[typing.Literal["m"]] = C(default = "m")

@dataclass(frozen=True, kw_only=True)
class RawStrConfigCls(CustomConfDatacls):
    accessibility: C[Accessibility] = C(default = "enable_by_delimeter")
    delimeter_syntax: C[StringDelimeters] = C(default = "triple")
    prefix_syntax: C[typing.Literal["r", "l"]] = C(default = "r")

@dataclass(frozen=True, kw_only=True)
class ByteStrConfigCls(CustomConfDatacls):
    _parent: typing.ClassVar[LiteralsConfigCls]
    accessibility: C[Accessibility] = C(default = "enable_by_delimeter")
    delimeter_syntax: C[StringDelimeters] = C(default = "triple")
    prefix_syntax: C[typing.Literal["b"]] = C(default = "b")

@dataclass(frozen=True, kw_only=True)
class StrEscapePatternConfigCls(CustomConfDatacls):
    _parent: typing.ClassVar[StrEscapeCharsConfigCls]
    null: C[typing.Literal["\\0", "`0", "^0",
                           "\\@", "`@", "^@",
                           None]] = C(default = "\\0")
    bell: C[typing.Literal["\\a", "`a", "^a",
                           "\\G", "`G", "^G",
                           "\\🔔", "`🔔", "^🔔",
                           None]] = C(default = "\\a")
    backscape: C[typing.Literal["\\b", "`b", "^b",
                                "\\H", "`H", "^H",
                                None]] = C(default = "\\b")
    horizontal_tabulation: C[typing.Literal["\\t", "`t", "^t",
                                            "\\I", "`I", "^I",
                                            None]] = C(default = "\\t")
    line_feed: C[typing.Literal["\\n", "`n", "^n",
                                "\\J", "`J", "^J",
                                None]] = C(default = "\\n")
    vertical_tabulation: C[typing.Literal["\\v", "`v", "^v",
                                          "\\K", "`K", "^K",
                                          None]] = C(default = "\\v")
    form_feed: C[typing.Literal["\\f", "`f", "^f",
                                "\\L", "`L", "^L",
                                None]] = C(default = "\\f")
    carriage_return: C[typing.Literal["\\r", "`r", "^r",
                                      "\\M", "`M", "^M",
                                      None]] = C(default = "\\r")
    escape: C[typing.Literal["\\e", "`e", "^e",
                             "\\[", "`[", "^[",
                             None]] = C(default = "\\e")
    backtick: C[typing.Literal["\\`", "``", "^`", None]] = C(default = "\\`")
    double_quote: C[typing.Literal["\\\"", "`\"", "^\"", None]] = C(default = "\\\"")
    single_quote: C[typing.Literal["\\'", "`'", "^'", None]] = C(default = "\\'")
    backslash: C[typing.Literal["\\\\", "^\\", "`\\", None]] = C(default = "\\\\")
    caret: C[typing.Literal["^^", "`^", "\\^", None]] = C(default = "\\^")
    dollar: C[typing.Literal["$$", "\\$", "`$", "^$", None]] = C(default = "\\$")
    hash: C[typing.Literal["#" "#", "\\#", "`#", "^#", None]] = C(default = "\\#")
    percent: C[typing.Literal["%%", "\\%", "`%", "^%", None]] = C(default = "\\%")

    open_parenthesis: C[typing.Literal["((", "\\(", "`(", "^(", None]] = C(default = "((")
    close_parenthesis: C[typing.Literal["))", "\\)", "`)", "^)", None]] = C(default = "))")
    open_square_bracket: C[typing.Literal["[[", "\\[", "`[", "^[", None]] = C(default = "[[")
    close_square_bracket: C[typing.Literal["]]", "\\]", "`]", "^]", None]] = C(default = "]]")
    open_curly_brace: C[typing.Literal["{{", "\\{", "`{", "^{", None]] = C(default = "{{")
    close_curly_brace: C[typing.Literal["}}", "\\}", "`}", "^}", None]] = C(default = "}}")
    open_angle_bracket: C[typing.Literal["<<", "\\<", "`<", "^<"]] = C(default = "<<")
    close_angle_bracket: C[typing.Literal[">>", "\\>", "`>", "^>"]] = C(default = "<<")

    def get_escape_dict(self, format_str: bool = False, raw_string: bool = False) -> dict[str, str]:
        dict_: dict[str, str] = {}
        s =  self._parent._parent
        delimeters = s.delimeters.get()
        name_lookup = {
            "\"": "double_quote",
            "'": "single_quote",
            "`": "backtick",
            "#": "hash",
            "$": "dollar",
            "%": "percent",
            "^": "caret",
            "(": "open_parenthesis",
            ")": "close_parenthesis",
            "[": "open_square_bracket",
            "]": "close_square_bracket",
            "{": "open_curly_brace",
            "}": "close_curly_brace",
            "<": "open_angle_bracket",
            ">": "close_angle_bracket"
        }
        for name in delimeters:
            dict_[getattr(self, name_lookup[name])] = name
        if format_str:
            interpo = s.interpolation
            if interpo.allow_identifier_syntax:
                ident_pref = interpo.identifier_prefix_syntax.get()
                dict_[getattr(self, name_lookup[ident_pref])] = ident_pref
            opening_sym = interpo.expression_syntax.start.get()[0]
            closing_sym = interpo.expression_syntax.end.get()[0]
            dict_[getattr(self, name_lookup[opening_sym[0]])] = opening_sym[0]
            dict_[getattr(self, name_lookup[closing_sym])] = closing_sym
        if not raw_string:
            p = [("null", "\0"), ("bell", "\a"), ("backscape", "\b"),
                 ("horizontal_tabulation", "\t"), ("line_feed", "\n"),
                 ("vertical_tabulation", "\v"), ("form_feed", "\f"),
                 ("carriage_return", "\r"), ("escape", "\x1b")
                ]
            dict_.update({getattr(self, name): char
                          for name, char in p
                          if getattr(self, name) is not None})
        return dict_

@dataclass(frozen=True, kw_only=True)
class StrEscapeCharsConfigCls(CustomConfDatacls):
    _parent: typing.ClassVar[StringLiteralsConfigCls]
    patterns: StrEscapePatternConfigCls = StrEscapePatternConfigCls()
    unused_patterns_behavior: C[typing.Literal["enforced", "ignore", "unenforced"]] = C(default = "ignore")

@dataclass(frozen=True, kw_only=True)
class StringLiteralsConfigCls(CustomConfDatacls):
    _parent: typing.ClassVar[LiteralsConfigCls]
    delimeters: C[StringDelimeters] = C(default = ("'", "`", '"'))
    interpolation: StrInterpolationConfigCls = StrInterpolationConfigCls()
    multiline: MultilineStrConfigCls = MultilineStrConfigCls()
    raw_string: RawStrConfigCls = RawStrConfigCls()
    byte_string: ByteStrConfigCls = ByteStrConfigCls()
    escape_pattern: StrEscapeCharsConfigCls = StrEscapeCharsConfigCls()

    def validate_config(self):
        for category, name in self._():
            if category.accessibility.get().endswith(""):
                for quote in category.delimeter_syntax.get():
                    if quote not in self.delimeters.get():
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
            if category.accessibility.get().endswith("prefix"):
                prefixes.append(category.prefix_syntax.get())
        delis = typing.cast(list[str], list(self.delimeters.get()[:])) # Pyright just smoke some weed today
        if self.multiline.delimeter_syntax.get() == "triple":
            if self.multiline.accessibility.get().endswith("delimeter"):
                delis.extend(dl*3 for dl in self.delimeters.get())
        for n in range(len(prefixes) + 1):
            for perm in itertools.permutations(prefixes, n):
                ls.extend(
                    "".join(perm)+quote for quote in delis
                )
        return ls

@dataclass(frozen=True, kw_only=True)
class EllipsisLiteralConfigCls(CustomConfDatacls):
    _parent: typing.ClassVar[LiteralsConfigCls]
    pass

@dataclass(frozen=True, kw_only=True)
class LiteralsConfigCls(CustomConfDatacls):
    _parent: typing.ClassVar[CustomizationConfigCls]
    numbers: NumberLiteralsConfigCls = NumberLiteralsConfigCls()
    booleans: BooleanLiteralsConfigCls = BooleanLiteralsConfigCls()
    null: NullLiteralConfigCls = NullLiteralConfigCls()
    strings: StringLiteralsConfigCls = StringLiteralsConfigCls()
    ellipsis: EllipsisLiteralConfigCls = EllipsisLiteralConfigCls()