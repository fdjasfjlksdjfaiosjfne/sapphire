from __future__ import annotations
from enum import Enum, auto, unique
import typing

from regex import compile, Pattern, match
from backend import errors

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

    def __hash__(self) -> int:
        return hash(self.type)

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
    For = auto()
    Cfor = auto()
    Scope = auto()
    In = auto()
    NotIn = auto()
    Return = auto()
    Match = auto()
    Case = auto()
    Break = auto()
    Continue = auto()
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
    LeftShift = auto()
    RightShift = auto()
    Coalescing = auto()
    Elvis = auto()
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

class RegexPatternConfiguration(typing.NamedTuple):
    patterns: typing.Tuple[Pattern]
    include_value: bool = False

def RPC(*patterns, include_value: str = False):
    return RegexPatternConfiguration(patterns, include_value)

regex_patterns: dict[TokenType, RegexPatternConfiguration] = {
    TokenType.NewLine: RPC(compile(r"[\r\n]+")),
    TokenType.NOTHING: RPC(
        compile(r"\t+"),
        compile(r" +"),
        compile("#.*"),
    ),
    # ^ Keywords
    TokenType.Let: RPC(compile("let")),
    TokenType.Const: RPC(compile("const")),
    TokenType.Fn: RPC(compile("fn")),
    TokenType.Class: RPC(compile("class")),
    TokenType.While: RPC(compile("while")),
    TokenType.For: RPC(compile("for")),
    TokenType.Cfor: RPC(compile("cfor")),
    TokenType.And: RPC(compile("and")),
    TokenType.Or: RPC(compile("or")),
    TokenType.Xor: RPC(compile("xor")),
    TokenType.Not: RPC(compile("not")),
    TokenType.In: RPC(compile("in")),
    TokenType.NotIn: RPC(compile("not in")),
    TokenType.Return: RPC(compile("return")),
    TokenType.If: RPC(compile("if")),
    TokenType.Elif: RPC(compile("elif")),
    TokenType.Else: RPC(compile("else")),
    TokenType.Match: RPC(compile("match")),
    TokenType.Case: RPC(compile("case")),
    TokenType.Break: RPC(compile("break")),
    TokenType.Continue: RPC(compile("continue")),
    # ^ Symbols
    TokenType.Spaceship: RPC(compile("<=>")),
    TokenType.LessEqualThan: RPC(compile("<=")),
    TokenType.GreaterEqualThan: RPC(compile(">=")),
    TokenType.LeftShift: RPC(compile("<<")),
    TokenType.RightShift: RPC(compile(">>")),
    TokenType.Elvis: RPC(compile(r"\?:")),
    TokenType.Coalescing: RPC(compile(r"\?{2}")),
    TokenType.Equal: RPC(compile("==")),
    TokenType.NotEqual: RPC(compile("!=")),
    TokenType.OpenParenthesis: RPC(compile(r"\(")),
    TokenType.CloseParenthesis: RPC(compile(r"\)")),
    TokenType.OpenSquareBracket: RPC(compile(r"\[")),
    TokenType.CloseSquareBracket: RPC(compile(r"\]")),
    TokenType.OpenCurlyBrace: RPC(compile(r"\{")),
    TokenType.CloseCurlyBrace: RPC(compile(r"\}")),
    TokenType.LessThan: RPC(compile("<")),
    TokenType.GreaterThan: RPC(compile(">")),
    TokenType.AssignOper: RPC(compile("=")),
    TokenType.ModifierAssignOper: RPC(
        compile(r"\+="),
        compile("-="),
        compile(r"\*="),
        compile("/="),
        compile(r"\*{2}="),
        include_value=True
    ),
    TokenType.WalrusOper: RPC(compile(":=")),
    TokenType.At: RPC(compile("@")),
    TokenType.Arrow: RPC(compile("->")),
    TokenType.Incre: RPC(compile(r"\+{2}")),
    TokenType.Decre: RPC(compile(r"\-{2}")),
    TokenType.Plus: RPC(compile(r"\+")),
    TokenType.Minus: RPC(compile("-")),
    TokenType.Exponentiation: RPC(compile(r"\*{2}")),
    TokenType.Asterisk: RPC(compile(r"\*")),
    TokenType.FloorDivision: RPC(compile("/{2}")),
    TokenType.TrueDivision: RPC(compile("/")),
    TokenType.Modulus: RPC(compile("%")),
    TokenType.Comma: RPC(compile(",")),
    TokenType.GDCologne: RPC(compile(":")),
    TokenType.Ellipsis: RPC(compile(r"\.{3}")),
    TokenType.Concanentation: RPC(compile(r"\.{2}")),
    TokenType.Dot: RPC(compile(r"\.")),
    TokenType.QuestionMark: RPC(compile(r"\?")),
    TokenType.Semicolon: RPC(compile(";")),
    TokenType.Andpersand: RPC(compile("&")),
    TokenType.VerticalBar: RPC(compile(r"\|")),
    TokenType.Caret: RPC(compile(r"\^")),
    # ^ Primitives and identifiers
    TokenType.Bool: RPC(compile("true"), compile("false"), include_value=True),
    TokenType.Null: RPC(compile("null")),
    TokenType.Str: RPC(
        compile(r"(?:r|f|fr|rf)?([\"'`])((?:[^\\]|\\.)*?)\1"), # Normal strings
        compile(r"(?:r|f|fr|rf)?(\"{3}|'{3}|`{3})((?:[^\\]|\\.|\n|\r)*?)\1"), # Multi-line strings
        include_value=True
    ),
    TokenType.Identifier: RPC(compile(r"[\p{L}_][\p{L}_\d]*"), include_value=True),
    TokenType.Float: RPC(compile(r"[\d_]*\.[\d_]+(e[\d_]+)?"), include_value=True),
    TokenType.Int: RPC(
            compile(r"[\d_]+"), 
            compile(r"0x[\da-fA-F_]+"),
            compile(r"0o[0-7_]+"),
            compile(r"0b[01_]+"),
            include_value=True
    ),
}

def tokenize(src: str) -> list[Token]:
    def snap(match, token_type: TokenType, include_match: bool = True) -> None:
        nonlocal src
        src = src[len(match):]
        tokens.append(Token(token_type, match if include_match else None))
    
    last_token = lambda: tokens[-1] if tokens else Token(TokenType.NOTHING)
    
    tokens = []
    while src:
        # ^ Multi-line comments
        if src.startswith("/*"):
            src = src[2:]
            nest = 1
            while src and nest > 0:
                if src.startwith("/*"):
                    nest += 1
                    src = src[2:]
                elif src.endswith("*/"):
                    nest -= 1
                    src = src[2:]
                else:
                    src = src[1:]
        
        # ^ Stuff that should be at the start of a line
        if last_token() == TokenType.NewLine:
            # > Decorators
            if mtch := match(f"@[{regex_patterns[TokenType.Identifier]}]"): 
                snap(mtch.group(), TokenType.Decorator)
            
            # > Labels
            elif mtch := match(f"{regex_patterns[TokenType.Identifier]}:"): 
                snap(mtch.group(), TokenType.Label)
        
        # ^ Everything else
        else:
            for token_type, dict_ in regex_patterns.items():
                for pattern in dict_.patterns:
                    if mtch := pattern.match(src):
                        snap(mtch.group(), token_type, dict_.include_value)
                        break
                else:
                    continue
                break
            else:
                raise errors.SyntaxError(f"Invalid character found: {src}")
    tokens = [token for token in tokens if token != TokenType.NOTHING]
    tokens.append(Token(TokenType.EoF))
    return tokens