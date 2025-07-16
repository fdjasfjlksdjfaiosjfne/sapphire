from __future__ import annotations
import ast

from enum import Enum, auto, unique
import types
import typing

from regex import compile # conveniece...
import regex
from backend import errors


class Token:
    def __init__(self, type: TokenType, value: str = ""):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f"Token(type={self.type.name}{f", value={self.value}" if self.value else ""})"
    
    def __ne__(self, other) -> bool:
        if isinstance(other, TokenType):
            return self.type != other
        if isinstance(other, Token):
            return self.type != other.type or self.value != other.value
        return NotImplemented
    
    def __eq__(self, other) -> bool:
        if isinstance(other, TokenType):
            return self.type == other
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
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
    Do = auto()
    Scope = auto()
    Throw = auto()
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
    patterns: typing.Tuple[regex.Pattern | str]
    include_value: bool = False

def RPC(*patterns, include_value: bool = False):
    return RegexPatternConfiguration(patterns, include_value)

regex_patterns: dict[TokenType, RegexPatternConfiguration] = {
    TokenType.NewLine: RPC(compile(r"[\r\n]+")),
    TokenType.NOTHING: RPC(
        compile(r"\t+"),
        compile(r" +"),
        compile("#.*"),
        compile(r"\\\n"),
    ),
    # ^ Keywords
    TokenType.Let: RPC("let"),
    TokenType.Const: RPC("const"),
    TokenType.Fn: RPC("fn"),
    TokenType.Class: RPC("class"),
    TokenType.While: RPC("while"),
    TokenType.For: RPC("for"),
    TokenType.Cfor: RPC("cfor"),
    TokenType.And: RPC("and"),
    TokenType.Or: RPC("or"),
    TokenType.Xor: RPC("xor"),
    TokenType.Not: RPC("not"),
    TokenType.In: RPC("in"),
    TokenType.NotIn: RPC("not in"),
    TokenType.Return: RPC("return"),
    TokenType.If: RPC("if"),
    TokenType.Elif: RPC("elif"),
    TokenType.Else: RPC("else"),
    TokenType.Match: RPC("match"),
    TokenType.Case: RPC("case"),
    TokenType.Break: RPC("break"),
    TokenType.Continue: RPC("continue"),
    TokenType.Throw: RPC("throw"),
    # ^ Symbols
    TokenType.Spaceship: RPC("<=>"),
    TokenType.LessEqualThan: RPC("<="),
    TokenType.GreaterEqualThan: RPC(">="),
    TokenType.LeftShift: RPC("<<"),
    TokenType.RightShift: RPC(">>"),
    TokenType.Equal: RPC("=="),
    TokenType.NotEqual: RPC("!="),
    TokenType.OpenParenthesis: RPC("("),
    TokenType.CloseParenthesis: RPC(")"),
    TokenType.OpenSquareBracket: RPC("["),
    TokenType.CloseSquareBracket: RPC("]"),
    TokenType.OpenCurlyBrace: RPC("{"),
    TokenType.CloseCurlyBrace: RPC("}"),
    TokenType.LessThan: RPC("<"),
    TokenType.GreaterThan: RPC(">"),
    TokenType.AssignOper: RPC("="),
    TokenType.ModifierAssignOper: RPC(
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
    TokenType.WalrusOper: RPC(":="),
    TokenType.At: RPC("@"),
    TokenType.Arrow: RPC("->"),
    TokenType.Incre: RPC("++"),
    TokenType.Decre: RPC(("--")),
    TokenType.Plus: RPC("+"),
    TokenType.Minus: RPC("-"),
    TokenType.Exponentiation: RPC(r"**"),
    TokenType.Asterisk: RPC("*"),
    TokenType.FloorDivision: RPC("//"),
    TokenType.TrueDivision: RPC("/"),
    TokenType.Modulus: RPC("%"),
    TokenType.Comma: RPC(","),
    TokenType.GDCologne: RPC(":"),
    TokenType.Ellipsis: RPC("..."),
    TokenType.Concanentation: RPC(".."),
    TokenType.Dot: RPC("."),
    TokenType.QuestionMark: RPC("?"),
    TokenType.Semicolon: RPC(";"),
    TokenType.Andpersand: RPC("&"),
    TokenType.VerticalBar: RPC("|"),
    TokenType.Caret: RPC(r"^"),
    # ^ Primitives and identifiers
    TokenType.Bool: RPC("true", "false", include_value=True),
    TokenType.Null: RPC("null"),
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
    )
}

class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.src = source[:]
        self.tokens = []
        self.token_index = 0
    
    def _emit_token(self, match: str, token_type: TokenType, include_match: bool = True) -> Token:
        self.src = self.src.lstrip(match)
        tok = Token(token_type, match if include_match else "")
        return tok

    def __iter__(self):
        return self

    def _lex_token(self) -> Token:
        if not self.src:
            return Token(TokenType.EoF)
        
        # ^ Multi-line comments
        if self.src.startswith("/*"):
            self.src = self.src[2:]
            nest = 1
            while self.src and nest > 0:
                if self.src.startswith("/*"):
                    nest += 1
                    self.src = self.src[2:]
                elif self.src.startswith("*/"):
                    nest -= 1
                    self.src = self.src[2:]
                else:
                    self.src = self.src[1:]
        
        # ^ Stuff that should be at the start of a line
        if len(self.tokens) > 0 and self.tokens[-1].type == TokenType.NewLine:
            # ^ Decorators
            if mtch := regex.match(f"@[{regex_patterns[TokenType.Identifier]}]", self.src):
                return self._emit_token(mtch.group(), TokenType.Decorator)
                
            # ^ Labels
            elif mtch := regex.match(f"{regex_patterns[TokenType.Identifier]}:", self.src):
                return self._emit_token(mtch.group(), TokenType.Label)

        # ^ Everything else
        for token_type, tple in regex_patterns.items():
            for pattern in tple.patterns:
                if isinstance(pattern, regex.Pattern):
                    cond = pattern.match(self.src)
                    if cond:
                        match = cond.group()
                    match = ""
                elif isinstance(pattern, str):
                    match = pattern
                    cond = self.src.startswith(pattern)
                else:
                    raise errors.InternalError(
                        f"regex_patterns contains invalid value ({pattern} from {token_type})")
                if cond:
                    return self._emit_token(match, token_type, tple.include_value)
        else:
            raise errors.SyntaxError(f"Invalid character found: U+{ord(self.src):x}")

    def peek(self, offset: int = 0) -> Token:
        while self.token_index + offset >= len(self.tokens):
            tok = self._lex_token()
            if tok.type == TokenType.NOTHING:
                continue
            self.tokens.append(tok)
            if tok.type == TokenType.EoF:
                break
        return self.tokens[self.token_index + offset]
    
    def advance(self, tok_types: typing.Sequence[TokenType] = [], error: errors.SapphireError | None = None) -> Token:
        tok = self.peek()
        if len(tok_types) != 0:
            if tok.type not in tok_types:
                if error is None:
                    raise errors.InternalError(
                        f"Error: {tok} doesn't match type specified: {tok_types}."
                        "If you see this error, it's probably either a redundant"
                        "fallback of the codebase got triggered or a guy forgot to"
                        "fill in the 'error' field of the eat()'s function call"
                    )
                raise error
        self.token_index += 1
        return tok
    
    def advance_matchings(self, tok_types: typing.Sequence[TokenType] = []):
        while self.peek().type in tok_types:
            self.advance()
    
    def remaining(self) -> str:
        return self.src[:]
    
    def consumed(self) -> str:
        return self.source.removesuffix(self.remaining())

    def save(self) -> int:
        return self.token_index
    
    def load(self, new_index) -> None:
        self.token_index = new_index

    def dump_all(self) -> list[Token]:
        while self.peek().type != TokenType.EoF:
            self.advance()
        return self.tokens