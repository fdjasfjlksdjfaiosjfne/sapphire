import regex
from parser.lexer.data.pattern_injection import (
    TokenPattern,
    StringTokenPattern,
    RegExTokenPattern,
    inject_patterns
)


def _separate_patterns() -> tuple[list[StringTokenPattern], list[RegExTokenPattern]]:
    plain_list, regex_list = [], []
    for i in _default_token_patterns:
        if isinstance(i.pattern, str):
            plain_list.append(i)
        elif isinstance(i.pattern, regex.Pattern):
            regex_list.append(i)
    return plain_list, regex_list

def get_token_patterns() -> list[TokenPattern]:
    result = []
    processed = []
    plains, regexes = _separate_patterns()

    inject_patterns(plains, regexes)

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
                processed.append(related)
    return result + regexes

_default_token_patterns: list[TokenPattern] = [
    StringTokenPattern("(", ("Parentheses", "OpenParenthesis")),
    StringTokenPattern(")", ("Parentheses", "CloseParenthesis")),
    StringTokenPattern("[", ("Parentheses", "OpenSquareBracket")),
    StringTokenPattern("]", ("Parentheses", "CloseSquareBracket")),
    StringTokenPattern("{", ("Parentheses", "OpenCurlyBrace")),
    StringTokenPattern("}", ("Parentheses", "CloseCurlyBrace")),
    StringTokenPattern("let", ("Keywords", "Let")),
    StringTokenPattern("const", ("Keywords", "Const")),
    StringTokenPattern("fn", ("Keywords", "Fn")),
    StringTokenPattern("class", ("Keywords", "Class")),
    StringTokenPattern("enum", ("Keywords", "Enum")),
    StringTokenPattern("struct", ("Keywords", "Struct")),
    StringTokenPattern("if", ("Keywords", "If")),
    StringTokenPattern("elif", ("Keywords", "Elif")),
    StringTokenPattern("else if", ("Keywords", "ElseIf")),
    StringTokenPattern("elseif", ("Keywords", "Elseif")),
    StringTokenPattern("elsif", ("Keywords", "Elsif")),
    StringTokenPattern("else", ("Keywords", "Else")),
    StringTokenPattern("cfor", ("Keywords", "Cfor")),
    StringTokenPattern("for", ("Keywords", "For")),
    StringTokenPattern("while", ("Keywords", "While")),
    StringTokenPattern("from", ("Keywords", "From")),
    StringTokenPattern("del", ("Keywords", "Del")),
    StringTokenPattern("end", ("Keywords", "End")),
    StringTokenPattern("as", ("Keywords", "As")),
    StringTokenPattern("is", ("Keywords", "Is")),
    StringTokenPattern("in", ("Keywords", "In")),
    StringTokenPattern("do", ("Keywords", "Do")),
    StringTokenPattern("catch", ("Keywords", "Catch")),
    StringTokenPattern("try", ("Keywords", "Try")),
    StringTokenPattern("finally", ("Keywords", "Finally")),
    StringTokenPattern("from", ("Keywords", "From")),
    StringTokenPattern("import", ("Keywords", "Import")),
    StringTokenPattern("throw", ("Keywords", "Throw")),
    StringTokenPattern("not", ("Keywords", "Not")),
    StringTokenPattern("raise", ("Keywords", "Raise")),
    StringTokenPattern("except", ("Keywords", "Except")),
    StringTokenPattern("function", ("Keywords", "Function")),
    StringTokenPattern("func", ("Keywords", "Func")),
    StringTokenPattern("default", ("Keywords", "Default")),
    StringTokenPattern("fun", ("Keywords", "Fun")),
    StringTokenPattern("def", ("Keywords", "Def")),
    StringTokenPattern("cls", ("Keywords", "Cls")),
    StringTokenPattern("del", ("Keywords", "Del")),
    StringTokenPattern("end", ("Keywords", "End")),
    StringTokenPattern("or", ("Keywords", "Or")),
    StringTokenPattern("xor", ("Keywords", "Xor")),
    StringTokenPattern("and", ("Keywords", "And")),
    StringTokenPattern("switch", ("Keywords", "Switch")),
    StringTokenPattern("static", ("Keywords", "Static")),
    StringTokenPattern("global", ("Keywords", "Global")),
    StringTokenPattern("local", ("Keywords", "Local")),
    StringTokenPattern("nonlocal", ("Keywords", "Nonlocal")),
    StringTokenPattern("private", ("Keywords", "Private")),
    StringTokenPattern("protected", ("Keywords", "Protected")),
    StringTokenPattern("public", ("Keywords", "Public")),
    StringTokenPattern("break", ("Keywords", "Break")),
    StringTokenPattern("continue", ("Keywords", "Continue")),
    StringTokenPattern("match", ("Keywords", "Match")),
    StringTokenPattern("case", ("Keywords", "Case")),
    StringTokenPattern("scope", ("Keywords", "Scope")),
    StringTokenPattern("return", ("Keywords", "Return")),
    StringTokenPattern("goto", ("Keywords", "Goto")),
    StringTokenPattern("%", ("Symbols", "Percent")),
    StringTokenPattern("+", ("Symbols", "Plus")),
    StringTokenPattern("++", ("Symbols", "DoublePlus")),
    StringTokenPattern("-", ("Symbols", "Dash")),
    StringTokenPattern("--", ("Symbols", "DoubleDash")),
    StringTokenPattern("*", ("Symbols", "Asterisk")),
    StringTokenPattern("**", ("Symbols", "DoubleAsterisk")),
    StringTokenPattern("/", ("Symbols", "ForwardSlash")),
    StringTokenPattern("//", ("Symbols", "DoubleForwardSlash")),
    StringTokenPattern("&", ("Symbols", "Andpersand")),
    StringTokenPattern("^", ("Symbols", "Caret")),
    StringTokenPattern("|", ("Symbols", "VerticalBar")),
    StringTokenPattern("_", ("Symbols", "Underscore")),
    StringTokenPattern("@", ("Symbols", "At")),
    StringTokenPattern(".", ("Symbols", "Dot")),
    StringTokenPattern("..", ("Symbols", "DoubleDot")),
    StringTokenPattern("...", ("Symbols", "TripleDot")),
    StringTokenPattern("\\", ("Symbols", "BackSlash")),
    StringTokenPattern(":", ("Symbols", "Colon")),
    StringTokenPattern(";", ("Symbols", "Semicolon")),
    StringTokenPattern(",", ("Symbols", "Comma")),
    StringTokenPattern("?", ("Symbols", "QuestionMark")),
    StringTokenPattern("~", ("Symbols", "Tilda")),
    StringTokenPattern("!", ("Symbols", "Exclamation")),
    StringTokenPattern("!=", ("Symbols", "ExclamationAndEqual")),
    StringTokenPattern("::", ("Symbols", "DoubleColon")),
    StringTokenPattern(">", ("Symbols", "GreaterThan")),
    StringTokenPattern(">>", ("Symbols", "DoubleGreaterThan")),
    StringTokenPattern("<", ("Symbols", "LessThan")),
    StringTokenPattern("<<", ("Symbols", "DoubleLessThan")),
    StringTokenPattern(">=", ("Symbols", "GreaterThanAndEqual")),
    StringTokenPattern("<=", ("Symbols", "LessThanAndEqual")),
    StringTokenPattern("&&", ("Symbols", "DoubleAndpersand")),
    StringTokenPattern("||", ("Symbols", "DoubleVerticalBar")),
    StringTokenPattern("^^", ("Symbols", "DoubleCaret")),
    StringTokenPattern("b&", ("Symbols", "BAndAndpersand")),
    StringTokenPattern("b|", ("Symbols", "BAndVerticalBar")),
    StringTokenPattern("b^", ("Symbols", "BAndCaret")),
    StringTokenPattern("=", ("Symbols", "Equal")),
    StringTokenPattern("==", ("Symbols", "DoubleEqual")),
    StringTokenPattern("===", ("Symbols", "TripleEqual")),
    StringTokenPattern("~=", ("Symbols", "TildaAndEqual")),
    StringTokenPattern("!~=", ("Symbols", "ExclamationAndTildaAndEqual")),
    StringTokenPattern("~!=", ("Symbols", "TildaAndExclamationAndEqual")),
    StringTokenPattern("!==", ("Symbols", "ExclamationAndDoubleEqual")),
    StringTokenPattern("<>", ("Symbols", "Diamond")),
    StringTokenPattern("><", ("Symbols", "InvertedDiamond")),
    StringTokenPattern("<=>", ("Symbols", "SpaceCapsule")),
    StringTokenPattern(">=<", ("Symbols", "QuirkyLookingFace")),
    StringTokenPattern(":=", ("Symbols", "ColonAndEqual")),
    StringTokenPattern("+=", ("Symbols", "PlusAndEqual")),
    StringTokenPattern("-=", ("Symbols", "DashAndEqual")),
    StringTokenPattern("*=", ("Symbols", "AsteriskAndEqual")),
    StringTokenPattern("/=", ("Symbols", "ForwardSlashAndEqual")),
    StringTokenPattern("//=", ("Symbols", "DoubleForwardSlashAndEqual")),
    StringTokenPattern("%=", ("Symbols", "PercentAndEqual")),
    StringTokenPattern("**=", ("Symbols", "DoubleAsteriskAndEqual")),
    StringTokenPattern("|=", ("Symbols", "VerticalBarAndEqual")),
    StringTokenPattern("^=", ("Symbols", "CaretAndEqual")),
    StringTokenPattern("&=", ("Symbols", "AndpersandAndEqual")),
    StringTokenPattern("b|=", ("Symbols", "BAndVerticalBarAndEqual")),
    StringTokenPattern("b^=", ("Symbols", "BAndCaretAndEqual")),
    StringTokenPattern("b&=", ("Symbols", "BAndAndpersandAndEqual")),
    StringTokenPattern("..=", ("Symbols", "DoubleDotAndEqual")),
    StringTokenPattern("@=", ("Symbols", "AtAndEqual")),
    StringTokenPattern("=+", ("Symbols", "EqualAndPlus")),
    StringTokenPattern("=-", ("Symbols", "EqualAndDash")),
    StringTokenPattern("=*", ("Symbols", "EqualAndAsterisk")),
    StringTokenPattern("=/", ("Symbols", "EqualAndForwardSlash")),
    StringTokenPattern("=//", ("Symbols", "EqualAndDoubleForwardSlash")),
    StringTokenPattern("=%", ("Symbols", "EqualAndPercent")),
    StringTokenPattern("=**", ("Symbols", "EqualAndDoubleAsterisk")),
    StringTokenPattern("=|", ("Symbols", "EqualAndVerticalBar")),
    StringTokenPattern("=^", ("Symbols", "EqualAndCaret")),
    StringTokenPattern("=&", ("Symbols", "EqualAndAndpersand")),
    StringTokenPattern("=b|", ("Symbols", "EqualAndBAndVerticalBar")),
    StringTokenPattern("=b^", ("Symbols", "EqualAndBAndCaret")),
    StringTokenPattern("=b&", ("Symbols", "EqualAndBAndAndpersand")),
    StringTokenPattern("=..", ("Symbols", "EqualAndDoubleDot")),
    StringTokenPattern("=@", ("Symbols", "EqualAndAt")),
    StringTokenPattern("->", ("Arrow",)),
    StringTokenPattern("=>", ("FatArrow",)),
    RegExTokenPattern(regex.compile(r"is(\s|\\\n)+not"), ("Keywords", "IsNot")),
    RegExTokenPattern(regex.compile(r"not(\s|\\\n)+in"), ("Keywords", "NotIn")),
    RegExTokenPattern(regex.compile(r"#.*"), ("_IgnoreByTokenizer",)),
    RegExTokenPattern(regex.compile(r"[\r\n]+"), ("NewLine",)),
    RegExTokenPattern(regex.compile(r"(\s|\\\n)+"), ("_IgnoreByTokenizer",)),
    RegExTokenPattern(regex.compile(r"[\p{L}_][\p{L}_\d]*"), ("Identifier",)),
]