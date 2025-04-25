from __future__ import annotations
from regex import compile, Pattern
from enum import Enum, auto, unique
import typing

class Token:
    def __init__(self, type: TokenType, value: str | None = None):
        self.type = type
        self.value = value
    
    def __repr__(self) -> str:
        return f"\nToken(type={self.type.name}{"" if self.value is None else f", value={self.value}"})"
    
    def __ne__(self, value: TokenType) -> bool:
        if isinstance(value, TokenType):
            return self.type != value
        return NotImplemented
    
    def __eq__(self, value: TokenType) -> bool:
        if isinstance(value, TokenType):
            return self.type == value
        return NotImplemented

@unique
class TokenType(Enum):
    NOTHING = auto() # Used for tricking the lexer ig idk
    EoF = auto()
    Decorator = auto()
    Label = auto()
    Identifier = auto()
    NewLine = auto()
    # ^ Parentheses
    OpenParenthesis = auto()
    CloseParenthesis = auto()
    OpenSquareBracket = auto()
    CloseSquareBracket = auto()
    OpenCurlyBrace = auto()
    CloseCurlyBrace = auto()
    # ^ Keywords
    Let = auto()
    Const = auto()
    Fn = auto()
    Class = auto()
    Not = auto()
    And = auto()
    Or = auto()
    Xor = auto()
    If = auto()
    Elif = auto()
    Else = auto()
    While = auto()
    Match = auto()
    Case = auto()
    # ^ Symbols
    Plus = auto()
    Minus = auto()
    Asterisk = auto()
    TrueDivision = auto()
    FloorDivision = auto()
    Modulus = auto()
    Exponentiation = auto()
    At = auto()
    Comma = auto()
    Dot = auto()
    GDCologne = auto()
    Semicolon = auto()
    QuestionMark = auto()
    Tilda = auto()
    Exclamation = auto()
    Incre = auto()
    Decre = auto()
    Andpersand = auto()
    VerticalBar = auto()
    Caret = auto()
    Equal = auto()
    NotEqual = auto()
    LessThan = auto()
    GreaterThan = auto()
    LessEqualThan = auto()
    GreaterEqualThan = auto()
    Spaceship = auto()
    BinaryXor = auto()
    BinaryOr = auto()
    BinaryAnd = auto()
    AssignOper = auto()
    ModifierAssignOper = auto()
    WalrusOper = auto()
    Concanentation = auto()
    Arrow = auto()
    # ^ Primitives
    Bool = auto()
    Null = auto()
    Int = auto()
    Float = auto()
    Str = auto()
    Ellipsis = auto()

class RegExDictConfiguration(typing.TypedDict):
    patterns: typing.List[Pattern]
    include_value: bool = True

regex_patterns: typing.Dict[TokenType, RegExDictConfiguration] = {
    TokenType.NewLine: {
        "patterns": [
            compile(r"[\r\n]+"),
        ], 
        "include_value": False
    },
    TokenType.NOTHING: {
        "patterns": [
            compile(r"\t+"),
            compile(r" +"),
            compile("#.*"),
            compile(r"/\*[.\r\n]*(\*/)?")
        ],
        "include_value": False 
    },
    # ^ Keywords
    TokenType.Let: {"patterns": [compile("let")]},
    TokenType.Const: {"patterns": [compile("const")]},
    TokenType.Fn: {"patterns": [compile("fn")]},
    TokenType.Class: {"patterns": [compile("class")]},
    TokenType.And: {"patterns": [compile("and")]},
    TokenType.Or: {"patterns": [compile("or")]},
    TokenType.Xor: {"patterns": [compile("xor")]},
    TokenType.Not: {"patterns": [compile("not")]},
    TokenType.If: {"patterns": [compile("if")]},
    TokenType.Elif: {"patterns": [compile("elif")]},
    TokenType.Else: {"patterns": [compile("else")]},
    TokenType.Match: {"patterns": [compile("match")]},
    TokenType.Case: {"patterns": [compile("case")]},
    # ^ Symbols
    
    # match a {
    #   case 1 | 2 | 3 | 4 | 5: print("1 to 5")
    #   case 6..14: print("6 to 14")
    # }
    
    TokenType.LessEqualThan: {"patterns": [compile("<=")]},
    TokenType.GreaterEqualThan: {"patterns": [compile(">=")]},
    TokenType.Equal: {"patterns": [compile("==")]},
    TokenType.NotEqual: {"patterns": [compile("!=")]},
    TokenType.Spaceship: {"patterns": [compile("<=>")]},
    TokenType.OpenParenthesis: {"patterns": [compile(r"\(")]},
    TokenType.CloseParenthesis: {"patterns": [compile(r"\)")]},
    TokenType.OpenSquareBracket: {"patterns": [compile(r"\[")]},
    TokenType.CloseSquareBracket: {"patterns": [compile(r"\]")]},
    TokenType.OpenCurlyBrace: {"patterns": [compile(r"\{")]},
    TokenType.CloseCurlyBrace: {"patterns": [compile(r"\}")]},
    TokenType.LessThan: {"patterns": [compile("<")]},
    TokenType.GreaterThan: {"patterns": [compile(">")]},
    TokenType.AssignOper: {"patterns": [compile("=")]},
    
    TokenType.ModifierAssignOper: {
        "patterns": [
            compile(r"\+="),
            compile("-="),
            compile(r"\*="),
            compile("/="),
            compile(r"\*{2}="),
        ],
        "include_value": True
    },
    
    TokenType.WalrusOper: {"patterns": [compile(":=")]},
    TokenType.At: {"patterns": [compile("@")]},
    TokenType.Arrow: {"patterns": [compile("->")]},
    TokenType.Plus: {"patterns": [compile(r"\+")]},
    TokenType.Minus: {"patterns": [compile("-")]},
    TokenType.Exponentiation: {"patterns": [compile(r"\*{2}")]},
    TokenType.Asterisk: {"patterns": [compile(r"\*")]},
    TokenType.FloorDivision: {"patterns": [compile("/{2}")]},
    TokenType.TrueDivision: {"patterns": [compile("/")]},
    TokenType.Modulus: {"patterns": [compile("%")]},
    TokenType.Comma: {"patterns": [compile(",")]},
    TokenType.GDCologne: {"patterns": [compile(":")]},
    TokenType.Ellipsis: {"patterns": [compile(r"\.{3}")]},
    TokenType.Concanentation: {"patterns": [compile(r"\.{2}")]},
    TokenType.Dot: {"patterns": [compile(r"\.")]},
    TokenType.QuestionMark: {"patterns": [compile(r"\?")]},
    TokenType.Semicolon: {"patterns": [compile(";")]},
    TokenType.Andpersand: {"patterns": [compile("&")]},
    TokenType.VerticalBar: {"patterns": [compile(r"\|")]},
    TokenType.Caret: {"patterns": [compile(r"\^")]},
    
    # ^ Primitives and identifiers
    TokenType.Bool: {"patterns": [compile("true"), compile("false")], "include_value": True},
    TokenType.Null: {"patterns": [compile("null")]},
    TokenType.Str: {
        "patterns": [
        compile(r"(?:r|f|fr|rf)?([\"'`])((?:[^\\]|\\.)*?)\1"),
        compile(r"(?:r|f|fr|rf)?([\"'`]{3})((?:[^\\]|\\.|\n|\r)*?)\1")
        ],
        "include_value": True
    },
    TokenType.Identifier: {"patterns": [compile(r"[\p{L}_][\p{L}_\d]*")], "include_value": True},
    TokenType.Float: {"patterns": [compile(r"\d*\.\d+(e\d+)?")], "include_value": True},
    TokenType.Int: {
        "patterns": [
            compile(r"\d+"),
            compile(r"0x[\da-fA-F]+"), # Hexadecimals
            compile(r"0o[0-7]+"), # Octals
            compile(r"0b[01]+") # Binary
        ],
        "include_value": True
    },
}