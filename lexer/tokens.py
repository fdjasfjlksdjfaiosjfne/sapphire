from __future__ import annotations
from dataclasses import dataclass
from regex import compile, Pattern
from enum import *
from typing import *
from functools import *

@dataclass
class Token:
    type: TokenType
    value: str | None = None
    # @enforce_types
    def __repr__(self: Self) -> str:
        return f"\nToken(type={self.type.name}{"" if self.value is None else f", value={self.value}"})"
    
    def __ne__(self: Self, value: TokenType) -> bool:
        if isinstance(value, TokenType):
            return self.type != value
        return NotImplemented
    
    def __eq__(self: Self, value: TokenType) -> bool:
        if isinstance(value, TokenType):
            return self.type == value
        return NotImplemented
    
    def _in(self: Self, *types: Tuple[TokenType, ...]):
        return self.type in set(types)

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
    OpenAngleBracket = auto()
    CloseAngleBracket = auto()
    # ^ Keywords
    Let = auto()
    Const = auto()
    Fn = auto()
    Class = auto()
    Not = auto()
    # ^ Symbols
    Plus = auto()
    Minus = auto()
    Asterisk = auto()
    Divide = auto()
    Modulus = auto()
    Exponentiation = auto()
    Comma = auto()
    Dot = auto()
    Colon = auto()
    GDCologne = auto()
    Semicolon = auto()
    QuestionMark = auto()
    Tilda = auto()
    Exclamation = auto()
    Incre = auto()
    Decre = auto()
    AssignOper = auto()
    CompOper = auto()
    LogicalOper = auto()
    BinaryOper = auto()
    WalrusOper = auto()
    # ^ Primitives
    Bool = auto()
    Null = auto()
    Int = auto()
    Float = auto()
    Str = auto()
    Ellipsis = auto()

class RegExDictConfiguration(TypedDict):
    patterns: List[Pattern]
    include_value: bool = True

regex_patterns: Dict[TokenType, RegExDictConfiguration] = {
    TokenType.Decorator: {"patterns": [compile(r"[\n\r]+[\t ]*")]},
    TokenType.Label: {"patterns": [compile(r"[\n\r]+[\t ]*")]},
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
            compile("//.*"),
            compile(r"/\*[.\s]*(\*/)?")
        ],
        "include_value": False 
    },
    # ^ Keywords
    TokenType.Let: {"patterns": [compile("let")], "include_value": False},
    TokenType.Const: {"patterns": [compile("const")], "include_value": False},
    TokenType.Fn: {"patterns": [compile("fn")], "include_value": False},
    TokenType.Class: {"patterns": [compile("class")], "include_value": False},
    # ^ Symbols
    
    # match a {
    #   case 1 | 2 | 3 | 4 | 5: print("1 to 5")
    #   case 6..14: print("6 to 14")
    # }
    
    TokenType.LogicalOper: {
        "patterns": [
            compile("&"),
            compile("and"),
            compile(r"\|"),
            compile("or"),
            compile(r"\^"),
            compile("xor")
        ]
    },
    TokenType.OpenParenthesis: {"patterns": [compile(r"\(")], "include_value": False},
    TokenType.CloseParenthesis: {"patterns": [compile(r"\)")], "include_value": False},
    TokenType.OpenSquareBracket: {"patterns": [compile(r"\[")], "include_value": False},
    TokenType.CloseSquareBracket: {"patterns": [compile(r"\]")], "include_value": False},
    TokenType.OpenCurlyBrace: {"patterns": [compile(r"\{")], "include_value": False},
    TokenType.CloseCurlyBrace: {"patterns": [compile(r"\}")], "include_value": False},
    TokenType.OpenAngleBracket: {"patterns": [compile("<")], "include_value": False},
    TokenType.CloseAngleBracket: {"patterns": [compile(">")], "include_value": False},
    TokenType.CompOper: {
        "patterns": [
        compile(r"<=>"),
        compile(r">="),
        compile(r"<="),
        compile(r"=="),
        compile(r"!="),
        compile(r">"),
        compile(r"<")
        ]
    },
    TokenType.AssignOper: {
        "patterns": [
        ## Statements
        compile("="),
        compile("c="),
        compile("i="),
        compile(r"\+="),
        compile("-="),
        compile(r"\*="),
        compile("/="),
        compile(r"\*{2}="),
        ## Exprs
    ]},
    TokenType.WalrusOper: {
        "patterns": [
            compile(":="),
            compile("c:="),
            compile("i:=")
        ]
    },
    TokenType.Plus: {"patterns": [compile(r"\+")], "include_value": False},
    TokenType.Minus: {"patterns": [compile("-")], "include_value": False},
    TokenType.Exponentiation: {"patterns": [compile(r"\*{2}")], "include_value": False},
    TokenType.Asterisk: {"patterns": [compile(r"\*")], "include_value": False},
    TokenType.Divide: {"patterns": [compile("/")], "include_value": False},
    TokenType.Modulus: {"patterns": [compile("%")], "include_value": False},
    TokenType.Comma: {"patterns": [compile(",")], "include_value": False},
    TokenType.GDCologne: {"patterns": [compile(":")], "include_value": False},
    TokenType.Colon: {"patterns": [compile(":")], "include_value": False},
    TokenType.Ellipsis: {"patterns": [compile(r"\.{3}")], "include_value": False},
    TokenType.Dot: {"patterns": [compile(r"\.")], "include_value": False},
    TokenType.QuestionMark: {"patterns": [compile(r"\?")], "include_value": False},
    TokenType.Semicolon: {"patterns": [compile(";")], "include_value": False},
    # ^ Primitives and identifiers
    TokenType.Bool: {"patterns": [compile("true"), compile("false")]},
    TokenType.Null: {"patterns": [compile("null")], "include_value": False},
    TokenType.Str: {
        "patterns": [
        compile(r"(?:r|f|fr|rf)?([\"'`])((?:[^\\]|\\.)*?)\1"),
        compile(r"(?:r|f|fr|rf)?([\"'`]{3})((?:[^\\]|\\.|\n|\r)*?)\1")
        ]
    },
    TokenType.Identifier: {"patterns": [compile(r"[\p{L}_][\p{L}_\d]*")]},
    TokenType.Float: {"patterns": [compile(r"\d*\.\d+(e\d+)?")]},
    TokenType.Int: {
        "patterns": [
            compile(r"\d+"),
            compile(r"0x[\da-fA-F]+"), # Hexadecimals
            compile(r"0o[0-7]+"), # Octals
            compile(r"0b[01]+") # Binary
        ]
    },
}