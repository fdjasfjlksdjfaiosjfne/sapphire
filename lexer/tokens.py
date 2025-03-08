from dataclasses import dataclass
from regex import compile, Pattern
from enum import Enum
from typing import *
from backend.typecheck import enforce_types

Union

@dataclass
class Token:
    type: "TokenType"
    value: str | None = None
    @enforce_types
    def __repr__(self: Self) -> str:
        return f"\nToken(type={self.type.name}{"" if self.value is None else f", value={self.value}"})"

@dataclass
class Directive:
    name: str
    args: List[str]

class TokenType(Enum):
    NOTHING = None # Used for tricking the lexer ig idk
    EoF = "EoF"
    Decorator = "@Decorator"
    Label = "Label:"
    Directive = "#Directive"
    Identifier = "identifier"
    NewLine = r"\n"
    # ^ Parentheses
    OpenParenthesis = "("
    CloseParenthesis = ")"
    OpenSquareBracket = "["
    CloseSquareBracket = "]"
    OpenCurlyBrace = "{"
    CloseCurlyBrace = "}"
    # ^ Keywords
    Let = "let"
    Const = "const"
    Fn = "fn"
    Class = "class"
    Not = "not"
    # ^ Symbols
    Plus = "+"
    Minus = "-"
    Asterisk = "*"
    Divide = "/"
    Modulus = "%"
    Exponentiation = "**"
    Comma = ","
    Dot = "."
    Colon = ":"
    GDCologne = ":"
    Semicolon = ";"
    QuestionMark = "?"
    Tilda = "~"
    Exclamation = "!"
    Incre = "++"
    Decre = "--"
    AssignOper = ("=", "c=", "i=", ":=")
    CompOper = (">=, <=, ==, !=, <, >")
    LogicalOper = ("&", "^", "|")
    BinaryOper = ("b^", "b&", "b|", "<<", ">>")
    # ^ Primitives
    Bool = ("true", "false")
    Null = "null"
    Int = "int"
    Float = "float"
    Str = "str"
    Ellipsis = "ellipsis"

class RegExDictConfiguration(TypedDict):
    patterns: List[Pattern]
    include_value: bool = True

regex_patterns: Dict[TokenType, RegExDictConfiguration] = {
    TokenType.NewLine: {"patterns": [compile(r"[\n\r]+[\t ]*")], "include_value": False},
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
    TokenType.CompOper: {
        "patterns": [
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

