import dataclasses
from os import access
from backend import errors
import typing
import regex
from backend.config import CONFIG
import itertools

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

def permutations(
    possible_strs: list[str] | None = None,
    forbidden_matches: list[list[str]] | None = None,
    forced_strs: list[str] | None = None
) -> list[str]:
    """Return all permutations of a given characters.

    The optional `forbidden_matches` argument accept a list of lists, each containing
     strings. This'll allow you to get rid of permutations that have all characters
     contain in each list containing in it.

    For example: 
    - With [["f", "t"]], the permutation "ptl" and "fap" are allowed, but not "wtf".
    - With [["f", "t"], ["d", "r"]], the permutation "rt", "df" are allowed, but not 
    "ft", not "dr".

    The optional `forbidden_matches` argument accept a list of strings. This'll allow
     you to get rid of permutatons that does not have all of the forced strings.
    """
    possible_strs = possible_strs or []
    forbidden_matches = forbidden_matches or []
    forced_strs = forced_strs or []
    res = []
    # Generate all non-empty permutations
    for n in range(1 + min(len(f) for f in forced_strs),
                   len(possible_strs) + 1):
        # & itertools saves the day again
        for perm in itertools.permutations(possible_strs, n):
            skip = False
            # ? Check if this permutation contains any elements of any forced match
            if not all(f in perm for f in forced_strs):
                skip = True
            # ? Check if this permutation contains all elements of any forbidden match
            for forbidden in forbidden_matches:
                if all(f in perm for f in forbidden):
                    skip = True
                    break
            
            if not skip:
                prefix = ''.join(perm)
                if prefix not in res:
                    res.append(prefix)
    return res

def _str_regex(possible_formats: list[str] | None = None,
               forbidden_matches: list[list[str]] | None = None,
               forced_strs: list[str] | None = None,
               quotes: str = "\"'`",
               multiline: bool = False) -> regex.Pattern:
    str_prefixes = "|".join(permutations(possible_formats, forbidden_matches, forced_strs))
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

    def append_regex(formats, forbidden, forced=None, quotes="", multiline=False):
        regexes.append(
            RegExTokenPattern(
                _str_regex(formats, forbidden, forced, quotes, multiline),
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
        append_regex(possible_formats, forbidden_matches, [prefix], quotes=delimeters, multiline=False)
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