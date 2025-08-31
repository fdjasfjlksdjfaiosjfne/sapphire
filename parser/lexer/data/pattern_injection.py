import dataclasses
from backend import errors
import typing
import regex

from backend.config import CONFIG
from parser.lexer import utils

cus = CONFIG.customization



@dataclasses.dataclass
class StringTokenPattern:
    pattern: str
    associated_type: tuple[str, ...]

@dataclasses.dataclass
class RegExTokenPattern:
    pattern: regex.Pattern
    associated_type: tuple[str, ...]
    def __post_init__(self):
        if isinstance(self.pattern, str):
            self.pattern = regex.compile(self.pattern)

# $ These are used so much I need to put the TypeVars here
S = typing.TypeVar("S", bound = list[StringTokenPattern])
R = typing.TypeVar("R", bound = list[RegExTokenPattern])

def _booleans(plains: S, regexes: R) -> tuple[S, R]:
    bool_conf = cus.literals.booleans
    # ^ Booleans
    if bool_conf.enabled.get_value():
        true = bool_conf.syntax.true.get_value()
        false = bool_conf.syntax.false.get_value()
        if bool_conf.case_insensivity.get_value():
            regexes.append(RegExTokenPattern(
                regex.compile(f"({true}|{false})", regex.IGNORECASE),
                ("Primitives", "Boolean")
            ))
        else:
            plains.append(StringTokenPattern(true, ("Primitives", "Boolean")))
            plains.append(StringTokenPattern(false, ("Primitives", "Boolean")))
    return plains, regexes

def _null(plains: S, regexes: R) -> tuple[S, R]:
    null_conf = cus.literals.null
    if null_conf.enabled.get_value():
        null = null_conf.syntax.get_value()
        if null_conf.case_insensivity:
            regexes.append(RegExTokenPattern(
                regex.compile(null, regex.IGNORECASE),
                ("Primitives", "Null")
            ))
        else:
            plains.append(StringTokenPattern(null, ("Primitives", "Null")))
    return plains, regexes

def _str_regex(str_prefixes: str,
               quotes: str = "\"'`",
               multiline: bool = False) -> regex.Pattern:
    
    return regex.compile(
        fr"""
        (?:{str_prefixes})
        ([{quotes}])
        (?:
            (?:
            [^\\]
            | \\.
            {"|\r|\n" if multiline else ""}
            )
        )
        \1
        """,
        regex.VERBOSE | regex.DOTALL
    )

def _str(plains: S, regexes: R) -> tuple[S, R]:
    # ^ Strings
    str_conf = cus.literals.strings
    delimeters_list = str_conf.delimeters
    delimeters = "".join(delimeters_list)
    possible_formats = ["r", "b"]
    forbidden_matches = []

    def append_regex(formats, forbidden, quotes="", multiline=False):
        str_prefixes = "|".join(utils.permutations(formats, forbidden))
        regexes.append(
            RegExTokenPattern(
                _str_regex(str_prefixes, quotes, multiline),
                ("Primitives", "String")
            )
        )

    accessibility = str_conf.multiline.accessibility.get_value()

    if accessibility == "never":
        # Only append the non-multistring version
        append_regex(possible_formats, forbidden_matches, quotes=delimeters, multiline=False)
    elif accessibility == "always":
        # Only append the multistring version
        append_regex(possible_formats, forbidden_matches, quotes=delimeters, multiline=True)
    elif accessibility.endswith("prefix"):
        prefix = str_conf.multiline.prefix_syntax.get_value()
        pf = [fmt for fmt in possible_formats if fmt != prefix]
        append_regex(pf, forbidden_matches, quotes=delimeters, multiline=True)
        str_prefixes = (i for i in utils.permutations(possible_formats, forbidden_matches) if prefix in i)
        regexes.append(
            RegExTokenPattern(
                _str_regex(str_prefixes = "|".join(str_prefixes)),
                ("Primitives", "String")
            )
        )
        append_regex(possible_formats, forbidden_matches, quotes=delimeters, multiline=False)
    elif accessibility == "enable_by_prefix":
        append_regex(possible_formats, forbidden_matches, quotes=delimeters, multiline=False)
    elif accessibility.endswith("delimeter"):
        special_delims = str_conf.multiline.delimeter_syntax.get_value()
        if special_delims == "triple":
            multi_delims = [d * 3 for d in delimeters_list]
            single_delims = delimeters
        elif all(d in delimeters for d in special_delims):
            multi_delims = special_delims
            single_delims = "".join([d for d in delimeters_list if d not in multi_delims])
        else:
            raise errors.InternalError

        multi_delims_str = "".join(multi_delims)
        single_delims_str = "".join(single_delims)
        append_regex(possible_formats, forbidden_matches, quotes=multi_delims_str, multiline=accessibility.startswith("disable"))
        append_regex(possible_formats, forbidden_matches, quotes=single_delims_str, multiline=accessibility.startswith("enable"))

    return plains, regexes

def _numbers(plains: S, regexes: R) -> tuple[S, R]:
    nums_conf = cus.literals.numbers
    if nums_conf.numeric_separator.enabled:
        separator = nums_conf.numeric_separator.syntax
    else:
        separator = ""
    scientific_regex = rf"(e[\d{separator}]+)?"
    s = scientific_regex if nums_conf.scientific_notation else ""
    
    regexes.append(
        RegExTokenPattern(
            regex.compile(
                fr"""(?x)
                [\d{separator}]+
                \.[\d{separator}]+
                {s}
                """
            ),
            ("Primitives", "Float")
        )
    )

    # ^ Integers
    if nums_conf.integer_base_literals.binary:
        regexes.append(
            RegExTokenPattern(
                regex.compile(f"0b[01{separator}]+"),
                ("Primitives", "Int")
            )
        )
    if nums_conf.integer_base_literals.octal:
        regexes.append(
            RegExTokenPattern(
                regex.compile(f"0o[0-7{separator}]+"),
                ("Primitives", "Int")
            )
        )
    if nums_conf.integer_base_literals.hexadecimal:
        regexes.append(
            RegExTokenPattern(
                regex.compile(fr"(?i)0x[0-9a-f{separator}]+"),
                ("Primitives", "Int")
            )
        )
    if nums_conf.integer_base_literals.binary:
        regexes.append(
            RegExTokenPattern(
                regex.compile(fr"[\d{separator}]+"),
                ("Primitives", "Int")
            )
        )
    return plains, regexes

def _templates(plains: S, regexes: R) -> tuple[S, R]:
    if CONFIG.templates.inverted_comparisons != "disabled":
        plains += [
            StringTokenPattern("!<>", ("Templates", "InvertedComparisons", "EqualityWithDiamond")),
            StringTokenPattern("!><", ("Templates", "InvertedComparisons", "EqualityWithInvertedDiamond")),
            StringTokenPattern("!>=", ("Templates", "InvertedComparisons", "LessThan")),
            StringTokenPattern("!<=", ("Templates", "InvertedComparisons", "GreaterThan")),
            StringTokenPattern("!<", ("Templates", "InvertedComparisons", "GreaterThanOrEqualTo")),
            StringTokenPattern("!>", ("Templates", "InvertedComparisons", "LessThanOrEqualTo")),
        ]
    return plains, regexes

def _single_line_comments(plains: S, regexes: R) -> tuple[S, R]:
    ilc = cus.comments.inline_comment
    if ilc.enabled:
        space = " " if ilc.space_required else ""
        regexes.append(RegExTokenPattern(
            regex.compile(f"{ilc.syntax}{space}.*"),
            ("_IgnoreByTokenizer",)
        ))
    return plains, regexes

def inject_patterns(p: S, r: R) -> tuple[S, R]:
    _numbers(p, r)
    _str(p, r)
    _null(p, r)
    _booleans(p, r)
    _templates(p, r)
    _single_line_comments(p, r)
    return p, r