import dataclasses
import regex
from utils.config import CONFIG
from parser._lexer.symbol_tokens import InternalTokenType, ITTTypeChecking

class TokenPattern:
    pattern: str | regex.Pattern
    associated_type: ITTTypeChecking

@dataclasses.dataclass
class StringTokenPattern:
    pattern: str
    associated_type: ITTTypeChecking

@dataclasses.dataclass
class RegExTokenPattern:
    pattern: regex.Pattern
    associated_type: ITTTypeChecking

def _separate_patterns() -> tuple[list[StringTokenPattern], list[RegExTokenPattern]]:
    plain_list, regex_list = [], []
    for i in _default_token_patterns:
        if isinstance(i.pattern, str):
            plain_list.append(i)
        elif isinstance(i.pattern, regex.Pattern):
            regex_list.append(i)
    return plain_list, regex_list

def _inject_patterns(plains: list[StringTokenPattern], regexes: list[RegExTokenPattern]):
    # Booleans
    true = CONFIG.language_customization.redefine.true
    false = CONFIG.language_customization.redefine.false
    if CONFIG.language_customization.case_insensitive_booleans:
        regexes.append(RegExTokenPattern(
            regex.compile(f"({true}|{false})", regex.IGNORECASE),
            InternalTokenType.Primitives.Boolean
        ))
    else:
        plains.append(StringTokenPattern(true, InternalTokenType.Primitives.Boolean))
        plains.append(StringTokenPattern(false, InternalTokenType.Primitives.Boolean))

    null = CONFIG.language_customization.redefine.null
    if CONFIG.language_customization.case_insensitive_null:
        regexes.append(RegExTokenPattern(
            regex.compile(null, regex.IGNORECASE),
            InternalTokenType.Primitives.Null
        ))
    else:
        plains.append(StringTokenPattern(null, InternalTokenType.Primitives.Boolean))
    
    # & No need to return anything
    # & The list will be modified upon calling anyway
    # & ...right?

def get_token_patterns():
    result = []
    processed = set()
    plains, regexes = _separate_patterns()

    _inject_patterns(plains, regexes)

    # ^ Sort the plain text by prefixes
    plains_sorted_by_length = sorted(plains, key = lambda x: len(x.pattern))
    for pattern in plains_sorted_by_length:
        if pattern in processed:
            continue

        related_patterns = filter(
            lambda p: (p.pattern.startswith(pattern.pattern) 
                       or pattern.pattern.startswith(p.pattern)),
            plains
        )

        related_patterns = sorted(related_patterns, key = lambda x: len(x.pattern))
        for related in related_patterns:
            if related not in processed:
                result.append(related)
                processed.add(related)
    return result + regexes

_default_token_patterns = [
    StringTokenPattern("(", InternalTokenType.Parentheses.OpenParenthesis),
    StringTokenPattern(")", InternalTokenType.Parentheses.CloseParenthesis),
    StringTokenPattern("[", InternalTokenType.Parentheses.OpenSquareBracket),
    StringTokenPattern("]", InternalTokenType.Parentheses.CloseSquareBracket),
    StringTokenPattern("{", InternalTokenType.Parentheses.OpenCurlyBrace),
    StringTokenPattern("}", InternalTokenType.Parentheses.CloseCurlyBrace),
    StringTokenPattern("let", InternalTokenType.Keywords.Let),
    StringTokenPattern("const", InternalTokenType.Keywords.Const),
    StringTokenPattern("fn", InternalTokenType.Keywords.Fn),
    StringTokenPattern("class", InternalTokenType.Keywords.Class),
    StringTokenPattern("enum", InternalTokenType.Keywords.Enum),
    StringTokenPattern("struct", InternalTokenType.Keywords.Struct),
    StringTokenPattern("if", InternalTokenType.Keywords.If),
    StringTokenPattern("elif", InternalTokenType.Keywords.Elif),
    StringTokenPattern("else", InternalTokenType.Keywords.Else),
    StringTokenPattern("cfor", InternalTokenType.Keywords.Cfor),
    StringTokenPattern("for", InternalTokenType.Keywords.For),
    StringTokenPattern("while", InternalTokenType.Keywords.While),
    StringTokenPattern("from", InternalTokenType.Keywords.From),
    StringTokenPattern("del", InternalTokenType.Keywords.Del),
    StringTokenPattern("end", InternalTokenType.Keywords.End),
    StringTokenPattern("as", InternalTokenType.Keywords.As),
    StringTokenPattern("is", InternalTokenType.Keywords.Is),
    StringTokenPattern("in", InternalTokenType.Keywords.In),
    StringTokenPattern("do", InternalTokenType.Keywords.Do),
    StringTokenPattern("catch", InternalTokenType.Keywords.Catch),
    StringTokenPattern("try", InternalTokenType.Keywords.Try),
    StringTokenPattern("finally", InternalTokenType.Keywords.Finally),
    StringTokenPattern("from", InternalTokenType.Keywords.From),
    StringTokenPattern("import", InternalTokenType.Keywords.Import),
    StringTokenPattern("throw", InternalTokenType.Keywords.Throw),
    StringTokenPattern("not", InternalTokenType.Keywords.Not),
    StringTokenPattern("raise", InternalTokenType.Keywords.Raise),
    StringTokenPattern("except", InternalTokenType.Keywords.Except),
    StringTokenPattern("function", InternalTokenType.Keywords.Function),
    StringTokenPattern("func", InternalTokenType.Keywords.Func),
    StringTokenPattern("default", InternalTokenType.Keywords.Default),
    StringTokenPattern("fun", InternalTokenType.Keywords.Fun),
    StringTokenPattern("def", InternalTokenType.Keywords.Def),
    StringTokenPattern("cls", InternalTokenType.Keywords.Cls),
    StringTokenPattern("del", InternalTokenType.Keywords.Del),
    StringTokenPattern("end", InternalTokenType.Keywords.End),
    StringTokenPattern("switch", InternalTokenType.Keywords.Switch),
    StringTokenPattern("+", InternalTokenType.Symbols.Plus),
    StringTokenPattern("++", InternalTokenType.Symbols.DoublePlus),
    StringTokenPattern("-", InternalTokenType.Symbols.Dash),
    StringTokenPattern("--", InternalTokenType.Symbols.DoubleDash),
    StringTokenPattern("*", InternalTokenType.Symbols.Asterisk),
    StringTokenPattern("**", InternalTokenType.Symbols.DoubleAsterisk),
    StringTokenPattern("/", InternalTokenType.Symbols.ForwardSlash),
    StringTokenPattern("//", InternalTokenType.Symbols.DoubleForwardSlash),
    StringTokenPattern("&", InternalTokenType.Symbols.Andpersand),
    StringTokenPattern("^", InternalTokenType.Symbols.Caret),
    StringTokenPattern("|", InternalTokenType.Symbols.VerticalBar),
    StringTokenPattern("_", InternalTokenType.Symbols.Underscore),
    StringTokenPattern("@", InternalTokenType.Symbols.At),
    StringTokenPattern(".", InternalTokenType.Symbols.Dot),
    StringTokenPattern("..", InternalTokenType.Symbols.DoubleDot),
    StringTokenPattern("...", InternalTokenType.Symbols.TripleDot),
    StringTokenPattern("\\", InternalTokenType.Symbols.BackSlash),
    StringTokenPattern(":", InternalTokenType.Symbols.Colon),
    StringTokenPattern("::", InternalTokenType.Symbols.DoubleColon),
    StringTokenPattern(">", InternalTokenType.Symbols.GreaterThan),
    StringTokenPattern(">>", InternalTokenType.Symbols.DoubleGreaterThan),
    StringTokenPattern("<", InternalTokenType.Symbols.LessThan),
    StringTokenPattern("<<", InternalTokenType.Symbols.DoubleLessThan),
    StringTokenPattern(">=", InternalTokenType.Symbols.GreaterThanAndEqual),
    StringTokenPattern("<=", InternalTokenType.Symbols.LessThanAndEqual),
    StringTokenPattern("&&", InternalTokenType.Symbols.DoubleAndpersand),
    StringTokenPattern("||", InternalTokenType.Symbols.DoubleVerticalBar),
    StringTokenPattern("^^", InternalTokenType.Symbols.DoubleCaret),
    StringTokenPattern("b&", InternalTokenType.Symbols.BAndAndpersand),
    StringTokenPattern("b|", InternalTokenType.Symbols.BAndVerticalBar),
    StringTokenPattern("b^", InternalTokenType.Symbols.BAndCaret),
    StringTokenPattern("=", InternalTokenType.Symbols.Equal),
    StringTokenPattern("==", InternalTokenType.Symbols.DoubleEqual),
    StringTokenPattern("===", InternalTokenType.Symbols.TripleEqual),
    StringTokenPattern("<>", InternalTokenType.Symbols.Diamond),
    StringTokenPattern("><", InternalTokenType.Symbols.InvertedDiamond),
    StringTokenPattern("<=>", InternalTokenType.Symbols.SpaceCapsule),
    StringTokenPattern(">=<", InternalTokenType.Symbols.QuirkyLookingFace),
    StringTokenPattern(":=", InternalTokenType.Symbols.ColonAndEqual),
    StringTokenPattern("+=", InternalTokenType.Symbols.PlusAndEqual),
    StringTokenPattern("-=", InternalTokenType.Symbols.DashAndEqual),
    StringTokenPattern("*=", InternalTokenType.Symbols.AsteriskAndEqual),
    StringTokenPattern("/=", InternalTokenType.Symbols.ForwardSlashAndEqual),
    StringTokenPattern("//=", InternalTokenType.Symbols.DoubleForwardSlashAndEqual),
    StringTokenPattern("%=", InternalTokenType.Symbols.PercentAndEqual),
    StringTokenPattern("**=", InternalTokenType.Symbols.DoubleAsteriskAndEqual),
    StringTokenPattern("|=", InternalTokenType.Symbols.VerticalBarAndEqual),
    StringTokenPattern("^=", InternalTokenType.Symbols.CaretAndEqual),
    StringTokenPattern("&=", InternalTokenType.Symbols.AndpersandAndEqual),
    StringTokenPattern("b|=", InternalTokenType.Symbols.BAndVerticalBarAndEqual),
    StringTokenPattern("b^=", InternalTokenType.Symbols.BAndCaretAndEqual),
    StringTokenPattern("b&=", InternalTokenType.Symbols.BAndAndpersandAndEqual),
    StringTokenPattern("=+", InternalTokenType.Symbols.EqualAndPlus),
    StringTokenPattern("=-", InternalTokenType.Symbols.EqualAndDash),
    StringTokenPattern("=*", InternalTokenType.Symbols.EqualAndAsterisk),
    StringTokenPattern("=/", InternalTokenType.Symbols.EqualAndForwardSlash),
    StringTokenPattern("=//", InternalTokenType.Symbols.EqualAndDoubleForwardSlash),
    StringTokenPattern("=%", InternalTokenType.Symbols.EqualAndPercent),
    StringTokenPattern("=**", InternalTokenType.Symbols.EqualAndDoubleAsterisk),
    StringTokenPattern("=|", InternalTokenType.Symbols.EqualAndVerticalBar),
    StringTokenPattern("=^", InternalTokenType.Symbols.EqualAndCaret),
    StringTokenPattern("=&", InternalTokenType.Symbols.EqualAndAndpersand),
    StringTokenPattern("=b|", InternalTokenType.Symbols.EqualAndBAndVerticalBar),
    StringTokenPattern("=b^", InternalTokenType.Symbols.EqualAndBAndCaret),
    StringTokenPattern("=b&", InternalTokenType.Symbols.EqualAndBAndAndpersand),
    RegExTokenPattern(regex.compile(r"is(\s|\\\n)+not"), InternalTokenType.Keywords.IsNot),
    RegExTokenPattern(regex.compile(r"not(\s|\\\n)+in"), InternalTokenType.Keywords.NotIn),
    RegExTokenPattern(regex.compile(r"#.*"), InternalTokenType._IgnoreByTokenizer),
    RegExTokenPattern(regex.compile(r"[\r\n]+"), InternalTokenType.NewLine),
    RegExTokenPattern(regex.compile(r"(\s|\\\n)+"), InternalTokenType._IgnoreByTokenizer),
    
    RegExTokenPattern(
        regex.compile(r"""
                (?:r|b|br|rb)? # Optional raw or binary attribute, or both
                (\"{3}|'{3}|`{3}) # Accepts either a double quote, single quote, or backtick, three times fold
                (?:
                    (?: # This group attempts to prevent stray \
                        [^\\] # Anything that is NOT a stray backslash
                        |\\. # Any character (INCLUDING \n) that has a backslash before it
                        |\r|\n
                    )
                    *?) # A non-greedy quantifier to make sure it ends on the first valid quote
                \1 # Matches what it's matched on the first captured group, i.e. the group with the quotes
                """
                , regex.X | regex.S),
        InternalTokenType.Primitives.String
    ),

    RegExTokenPattern(
        # & Note that f-strings are parsed separately now
        # & Thanks, {}
        regex.compile(r"""
                (?:r|b|br|rb)? # Optional raw or binary attribute, or both
                ([\"'`]) # Accepts either a double quote, single quote, or backtick
                (?:
                    (?: # This group attempts to prevent stray \
                        [^\\\r\n] # Anything that is NOT a stray backslash, \r or \n
                        |\\. # Any character (INCLUDING \n) that has a backslash before it
                    )
                *?) # A non-greedy quantifier to make sure it ends on the first valid quote
                \1 # Matches what it's matched on the first captured group, i.e. the group with the quotes
                """,
                regex.VERBOSE | regex.DOTALL),
        InternalTokenType.Primitives.String
    ),
    
    RegExTokenPattern(regex.compile(r"[\p{L}_][\p{L}_\d]*"), InternalTokenType.Identifier),
    RegExTokenPattern(
        regex.compile(
            r"""(?x)
            [\d_]+ # The whole part
            \.[\d_]+ # The decimal part
            (e[\d_]+)? # The scientific notation part
            """
        ), InternalTokenType.Primitives.Float),
    RegExTokenPattern(regex.compile(r"[\d_]+"), InternalTokenType.Primitives.Int),
    RegExTokenPattern(regex.compile(r"0x[\da-fA-F_]+"), InternalTokenType.Primitives.Int),
    RegExTokenPattern(regex.compile(r"0o[0-7_]+"), InternalTokenType.Primitives.Int),
    RegExTokenPattern(regex.compile(r"0b[01_]+"), InternalTokenType.Primitives.Int)
]