from __future__ import annotations
import ast
import typing
import regex
from backend import errors
from parser.lexer.types import TokenType, get_regex_dict
from utils import config

TokenTypeSequence: typing.TypeAlias = (
    typing.Sequence[TokenType] 
    | typing.MutableSequence[TokenType]
    | typing.MutableSet[TokenType]
    | TokenType)

class Token:
    def __init__(self, type: TokenType, value: str = ""):
        self.type = type
        self.value = value

    def __str__(self) -> str: return repr(self)

    def __repr__(self) -> str:
        return f"Token(type={self.type.name}{f", value={self.value!r}" if self.value else ""})"
    
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

class Tokenizer:
    def __init__(self, source: str, conf: config.ConfigCls | None = None):
        self.source = source
        self.src = source[:]
        self.tokens = []
        self.token_index = 0
        self.regex_dict = get_regex_dict(conf or config.ConfigCls())
    
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
            if mtch := regex.match(f"@[{self.regex_dict[TokenType.Identifier]}]", self.src):
                return self._emit_token(mtch.group(), TokenType.Decorator)
                
            # ^ Labels
            elif mtch := regex.match(f"{self.regex_dict[TokenType.Identifier]}:", self.src):
                return self._emit_token(mtch.group(), TokenType.Label)

        # ^ Everything else
        for token_type, tple in self.regex_dict.items():
            for pattern in tple.patterns:
                if isinstance(pattern, regex.Pattern):
                    cond = pattern.match(self.src)
                    if cond:
                        match = cond.group()
                    else:
                        match = ""
                elif isinstance(pattern, str):
                    match = pattern
                    cond = self.src.startswith(pattern)
                else:
                    raise errors.InternalError(
                        f"self.regex_dict contains invalid value ({pattern} from {token_type})")
                if cond:
                    return self._emit_token(match, token_type, tple.include_value)
        else:
            raise errors.SyntaxError(f"Invalid character found: U+{ord(self.src):x}")

    def peek(self, offset: int = 0) -> Token:
        while self.token_index + offset >= len(self.tokens):
            tok = self._lex_token()
            if tok.type == TokenType.FORBIDDEN:
                continue
            self.tokens.append(tok)
            if tok.type == TokenType.EoF:
                break
        return self.tokens[self.token_index + offset]
    
    def advance(self, tok_types: TokenTypeSequence | None = None, error: errors.BaseSapphireError | None = None) -> Token:
        
        tok = self.peek()
        if tok_types is None: 
            tok_types = tuple()
        if isinstance(tok_types, TokenType):
            tok_types = (tok_types,)
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
    
    def advance_matchings(self, tok_types: TokenTypeSequence = []):
        if isinstance(tok_types, TokenType):
            tok_types = (tok_types,)
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