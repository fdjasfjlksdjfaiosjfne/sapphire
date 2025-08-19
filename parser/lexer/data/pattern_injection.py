import dataclasses
from backend import errors
import typing
import regex
from backend.config import CONFIG, CustomizationMode

cus = CONFIG.customization
redef = cus.redefine

@dataclasses.dataclass
class StringTokenPattern:
    pattern: str
    associated_type: tuple[str, ...]

@dataclasses.dataclass
class RegExTokenPattern:
    pattern: regex.Pattern
    associated_type: tuple[str, ...]

class TokenPattern(StringTokenPattern, RegExTokenPattern):
    pattern: str | regex.Pattern # pyright: ignore[reportIncompatibleVariableOverride]
    associated_type: tuple[str, ...]
    def __new__(cls, pattern: typing.Any, associated_type: tuple[str, ...]):
        if isinstance(pattern, str):
            return StringTokenPattern(pattern, associated_type)
        if isinstance(pattern, regex.Pattern):
            return RegExTokenPattern(pattern, associated_type)
        raise errors.InternalError(
            f"'pattern' is of invalid type ('{type(pattern)!r}')"
    )

S = typing.TypeVar("S", bound = list[StringTokenPattern])
R = typing.TypeVar("R", bound = list[RegExTokenPattern])

def _booleans(plains: S, regexes: R) -> tuple[S, R]:
    # ^ Booleans
    if cus.allow_booleans:
        true = redef.true
        false = redef.false
        if cus.case_insensitive_booleans:
            regexes.append(RegExTokenPattern(
                regex.compile(f"({true}|{false})", regex.IGNORECASE),
                ("Primitives", "Boolean")
            ))
        else:
            plains.append(StringTokenPattern(true, ("Primitives", "Boolean")))
            plains.append(StringTokenPattern(false, ("Primitives", "Boolean")))
    return plains, regexes

def _null(plains: S, regexes: R) -> tuple[S, R]:
    if cus.allow_null:
        null = redef.null
        if cus.case_insensitive_null:
            regexes.append(RegExTokenPattern(
                regex.compile(null, regex.IGNORECASE),
                ("Primitives", "Null")
            ))
        else:
            plains.append(StringTokenPattern(null, ("Primitives", "Null")))
    return plains, regexes

def _str[S: list[StringTokenPattern],
         R: list[RegExTokenPattern]](plains: S, regexes: R) -> tuple[S, R]:
    # ^ Strings
    quotes = "".join(cus.string_delimeters)
    if cus.multiline_strings == "default":
        # $ Strings are always multiline
        regexes.append(
            RegExTokenPattern(
                regex.compile(
                    r"""(?sx)
                    (?:r|b|br|rb)? # Optional raw or binary attribute, or both
                    [{}]
                    (?:
                        (?: # This group attempts to prevent stray \
                            [^\\] # Anything that is NOT a stray backslash
                            |\\. # Any character (INCLUDING \n) that has a backslash before it
                            |\r|\n
                        )
                        *?) # A non-greedy quantifier to make sure it ends on the first valid quote
                    \1 # Matches what it's matched on the first captured group, i.e. the group with the quotes
                    """.format(quotes)
                ),
                ("Primitives", "String")
            )
        )
    else:
        if cus.multiline_strings == "enabled":
            regexes.append(
                RegExTokenPattern(
                    regex.compile(
                        r"""(?sx)
                        (?:r|b|br|rb)? # Optional raw or binary attribute, or both
                        ({})
                        (?:
                            (?: # This group attempts to prevent stray \
                                [^\\] # Anything that is NOT a stray backslash
                                |\\. # Any character (INCLUDING \n) that has a backslash before it
                                |\r|\n
                            )
                            *?) # A non-greedy quantifier to make sure it ends on the first valid quote
                        \1 # Matches what it's matched on the first captured group, i.e. the group with the quotes
                        """.format("|".join(f"{i}{{3}}" for i in quotes))
                    ),
                    ("Primitives", "String")
                )
            )
        regexes.append(
            RegExTokenPattern(
                regex.compile(
                    r"""(?sx)
                    (?:r|b|br|rb)? # Optional raw or binary attribute, or both
                    ({})
                    (?:
                        (?: # This group attempts to prevent stray \
                            [^\\\r\n] # Anything that is NOT a stray backslash
                            |\\. # Any character (INCLUDING \n) that has a backslash before it
                        )
                        *?) # A non-greedy quantifier to make sure it ends on the first valid quote
                    \1 # Matches what it's matched on the first captured group, i.e. the group with the quotes
                    """.format(quotes)
                ),
                ("Primitives", "String")
            )
        )
    return plains, regexes

def _numbers(plains: S, regexes: R) -> tuple[S, R]:
    if cus.numeric_separator:
        separator = "_"
    else:
        separator = ""
    
    regexes.append(RegExTokenPattern(
        regex.compile(
            r"""(?x)
            [\d{}]+
            \.[\d{}]+
            {} # Scient
            """.format(separator,
                       separator,
                       rf"(e[\d{separator}]+)?" if cus.scientific_notation else "")),
        ("Primitives", "Float")
    ))

    if cus.integer_base_literals.binary:
        regexes.append(
            RegExTokenPattern(
                regex.compile(f"0b[01{separator}]+"),
                ("Primitives", "Int")
            )
        )
    if cus.integer_base_literals.octal:
        regexes.append(
            RegExTokenPattern(
                regex.compile(f"0o[0-7{separator}]+"),
                ("Primitives", "Int")
            )
        )
    if cus.integer_base_literals.hexadecimal:
        regexes.append(
            RegExTokenPattern(
                regex.compile(fr"(?i)0x[0-9a-f{separator}]+"),
                ("Primitives", "Int")
            )
        )
    if cus.integer_base_literals.binary:
        regexes.append(
            RegExTokenPattern(
                regex.compile(fr"[\d{separator}]+"),
                ("Primitives", "Int")
            )
        )
    return plains, regexes

def _templates(plains: S, regexes: R) -> tuple[S, R]:
    if CONFIG.templates.inverted_comparisons != CustomizationMode.Disabled:
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
    if redef.single_line_comment is not None:
        regexes.append(RegExTokenPattern(
            regex.compile(f"{redef.single_line_comment}.*"),
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