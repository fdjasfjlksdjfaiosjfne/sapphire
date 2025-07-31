from enum import Enum, auto, unique
import types
import dataclasses
import typing

from regex import compile # conveniece...
import regex
from backend import errors
from utils import config

class TokenType(Enum):
    FORBIDDEN = auto()
    EoF = auto()
    Decorator = auto()
    Label = auto()
    Identifier = auto()
    NewLine = auto()
    # ^ Parentheses
    PR_OpenParenthesis = auto()
    PR_CloseParenthesis = auto()
    PR_OpenSquareBracket = auto()
    PR_CloseSquareBracket = auto()
    PR_OpenCurlyBrace = auto()
    PR_CloseCurlyBrace = auto()
    # ^ KW - Keywords
    KW_Let = auto()
    KW_Const = auto()
    KW_FunctionDeclaration = auto()
    KW_ClassDeclaration = auto()
    KW_Not = auto()
    KW_And = auto()
    KW_Or = auto()
    KW_Xor = auto()
    KW_If = auto()
    KW_ElseIf = auto()
    KW_Else = auto()
    KW_Enum = auto()
    KW_WhileLoop = auto()
    KW_PythonFor = auto()
    KW_CFor = auto()
    KW_DoWhileLoop = auto()
    KW_As = auto()
    KW_Scope = auto()
    KW_Throw = auto()
    KW_From = auto()
    KW_Import = auto()
    KW_In = auto()
    KW_NotIn = auto()
    KW_Return = auto()
    KW_Match = auto()
    KW_Case = auto()
    KW_Break = auto()
    KW_Continue = auto()
    # ^ Symbols
    SY_Plus = auto()
    SY_Minus = auto()
    SY_Asterisk = auto()
    SY_FowardSlash = auto()
    SY_FloorDivision = auto()
    SY_Modulus = auto()
    SY_DoubleAsterisk = auto()
    SY_At = auto()
    SY_Comma = auto()
    SY_Dot = auto()
    SY_GDCologne = auto()
    SY_Semicolon = auto()
    SY_QuestionMark = auto()
    SY_Tilda = auto()
    SY_Exclamation = auto()
    SY_Incre = auto()
    SY_Decre = auto()
    SY_Andpersand = auto()
    SY_VerticalBar = auto()
    SY_Caret = auto()
    SY_Equal = auto()
    SY_NotEqual = auto()
    SY_LessThan = auto()
    SY_GreaterThan = auto()
    SY_LessEqualThan = auto()
    SY_GreaterEqualThan = auto()
    SY_Spaceship = auto()
    SY_BinaryXor = auto()
    SY_BinaryOr = auto()
    SY_BinaryAnd = auto()
    SY_LeftShift = auto()
    SY_RightShift = auto()
    SY_AssignOper = auto()
    SY_ModifierAssignOper = auto()
    SY_Walrus = auto()
    SY_Concanentation = auto()
    SY_Arrow = auto()
    # ^ Primitives
    PV_Bool = auto()
    PV_Null = auto()
    PV_Int = auto()
    PV_Float = auto()
    PV_String = auto()
    PV_Ellipsis = auto()

@dataclasses.dataclass
class RegexPatternConfiguration:
    patterns: typing.List[regex.Pattern | str]
    include_value: bool = False

def RPC(*patterns, include_value: bool = False):
    return RegexPatternConfiguration(list(patterns), include_value)

def get_regex_dict(conf: config.ConfigCls):
    patterns = _default_regex_patterns.copy()
    # ^ Search for configuration modes first
    modes = conf.language_customization_modes
    if modes.inverted_operators:
        if modes.inverted_operators == config.CustomizationMode.Forced:
            # ? Remove the built-in implementations
            patterns[TokenType.SY_LessThan].patterns = []
            patterns[TokenType.SY_LessEqualThan].patterns = []
            patterns[TokenType.SY_Equal].patterns = []
            patterns[TokenType.SY_GreaterEqualThan].patterns = []
            patterns[TokenType.SY_GreaterThan].patterns = []
    
        patterns[TokenType.SY_LessThan].patterns.append("!>=")
        patterns[TokenType.SY_LessEqualThan].patterns.append("!>")
        patterns[TokenType.SY_Equal].patterns.append("!<>")
        patterns[TokenType.SY_GreaterEqualThan].patterns.append("!<")
        patterns[TokenType.SY_GreaterThan].patterns.append("!<=")
    # ^ Search for redefinition afterwards
    redefine = conf.language_customization.redefine
    patterns[TokenType.SY_NotEqual].patterns = [redefine.not_equal]
    patterns[TokenType.SY_Spaceship].patterns = [redefine.spaceship_operator]
    patterns[TokenType.KW_FunctionDeclaration].patterns = [redefine.function_def]
    patterns[TokenType.KW_ClassDeclaration].patterns = [redefine.class_def]
    patterns[TokenType.KW_ElseIf].patterns = [redefine.else_if]
    
    return patterns

_default_regex_patterns: dict[TokenType, RegexPatternConfiguration] = {
    TokenType.NewLine: RPC(compile(r"[\r\n]+")),
    TokenType.FORBIDDEN: RPC(
        compile(r"\t+"),
        compile(r" +"),
        compile("#.*"),
        compile(r"\\\n"),
    ),
    # ^ Keywords
    TokenType.KW_Let: RPC("let"),
    TokenType.KW_Const: RPC("const"),
    TokenType.KW_FunctionDeclaration: RPC("fn"),
    TokenType.KW_ClassDeclaration: RPC("class"),
    TokenType.KW_WhileLoop: RPC("while"),
    TokenType.KW_PythonFor: RPC("for"),
    TokenType.KW_CFor: RPC("cfor"),
    TokenType.KW_And: RPC("and"),
    TokenType.KW_Or: RPC("or"),
    TokenType.KW_Xor: RPC("xor"),
    TokenType.KW_Not: RPC("not"),
    TokenType.KW_Enum: RPC("enum"),
    TokenType.KW_In: RPC("in"),
    TokenType.KW_NotIn: RPC("not in"),
    TokenType.KW_Return: RPC("return"),
    TokenType.KW_If: RPC("if"),
    TokenType.KW_ElseIf: RPC("elif"),
    TokenType.KW_Else: RPC("else"),
    TokenType.KW_Match: RPC("match"),
    TokenType.KW_Case: RPC("case"),
    TokenType.KW_Break: RPC("break"),
    TokenType.KW_Continue: RPC("continue"),
    TokenType.KW_Throw: RPC("throw"),
    TokenType.KW_From: RPC("from"),
    TokenType.KW_Import: RPC("import"),
    TokenType.KW_As: RPC("as"),
    # ^ Symbols
    TokenType.SY_Spaceship: RPC("<=>"),
    TokenType.SY_LessEqualThan: RPC("<="),
    TokenType.SY_GreaterEqualThan: RPC(">="),
    TokenType.SY_LeftShift: RPC("<<"),
    TokenType.SY_RightShift: RPC(">>"),
    TokenType.SY_Equal: RPC("=="),
    TokenType.SY_NotEqual: RPC("!="),
    TokenType.PR_OpenParenthesis: RPC("("),
    TokenType.PR_CloseParenthesis: RPC(")"),
    TokenType.PR_OpenSquareBracket: RPC("["),
    TokenType.PR_CloseSquareBracket: RPC("]"),
    TokenType.PR_OpenCurlyBrace: RPC("{"),
    TokenType.PR_CloseCurlyBrace: RPC("}"),
    TokenType.SY_LessThan: RPC("<"),
    TokenType.SY_GreaterThan: RPC(">"),
    TokenType.SY_AssignOper: RPC("="),
    TokenType.SY_ModifierAssignOper: RPC(
        "+=", "=+",
        "-=", "=-",
        compile(r"\*{1,2}="),
        compile(r"=\*{1,2}"),
        compile(r"/{1,2}="),
        compile(r"=/{1,2}"),
        "|=", "=|",
        "&=", "=&",
        "^=", "=^",
        include_value=True
    ),
    TokenType.SY_Walrus: RPC(":="),
    TokenType.SY_At: RPC("@"),
    TokenType.SY_Arrow: RPC("->"),
    TokenType.SY_Incre: RPC("++"),
    TokenType.SY_Decre: RPC(("--")),
    TokenType.SY_Plus: RPC("+"),
    TokenType.SY_Minus: RPC("-"),
    TokenType.SY_DoubleAsterisk: RPC(r"**"),
    TokenType.SY_Asterisk: RPC("*"),
    TokenType.SY_FloorDivision: RPC("//"),
    TokenType.SY_FowardSlash: RPC("/"),
    TokenType.SY_Modulus: RPC("%"),
    TokenType.SY_Comma: RPC(","),
    TokenType.SY_GDCologne: RPC(":"),
    TokenType.PV_Ellipsis: RPC("..."),
    TokenType.SY_Concanentation: RPC(".."),
    TokenType.SY_Dot: RPC("."),
    TokenType.SY_QuestionMark: RPC("?"),
    TokenType.SY_Semicolon: RPC(";"),
    TokenType.SY_Andpersand: RPC("&"),
    TokenType.SY_VerticalBar: RPC("|"),
    TokenType.SY_Caret: RPC(r"^"),
    # ^ Primitives and identifiers
    TokenType.PV_Bool: RPC("true", "false", include_value=True),
    TokenType.PV_Null: RPC("null"),
    TokenType.PV_String: RPC(
        compile(r"(?:r|f|fr|rf)?([\"'`])((?:[^\\]|\\.)*?)\1"), # Normal strings
        compile(r"(?:r|f|fr|rf)?(\"{3}|'{3}|`{3})((?:[^\\]|\\.|\n|\r)*?)\1"), # Multi-line strings
        include_value=True
    ),
    TokenType.Identifier: RPC(compile(r"[\p{L}_][\p{L}_\d]*"), include_value=True),
    TokenType.PV_Float: RPC(compile(r"[\d_]*\.[\d_]+(e[\d_]+)?"), include_value=True),
    TokenType.PV_Int: RPC(
            compile(r"[\d_]+"),
            compile(r"0x[\da-fA-F_]+"),
            compile(r"0o[0-7_]+"),
            compile(r"0b[01_]+"),
            include_value=True
    )
}