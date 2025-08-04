from __future__ import annotations
import ast
import typing
import regex
from backend import errors
from parser._lexer.enum_classes import TokenTypeEnum
from parser._lexer.symbol_tokens import InternalTokenType
from parser._lexer.patterns import (
    get_token_patterns,
    StringTokenPattern,
    RegExTokenPattern,
    )
from utils import config

TokenTypeSequence: typing.TypeAlias = (
    typing.Sequence[TokenTypeEnum] 
    | typing.MutableSequence[TokenTypeEnum]
    | typing.MutableSet[TokenTypeEnum]
    | TokenTypeEnum)

class Token:
    def __init__(self, type: TokenTypeEnum, value: str = ""):
        self.type = type
        self.value = value

    def __str__(self) -> str: return repr(self)

    def __repr__(self) -> str:
        return f"Token(type={self.type.name}{f", value={self.value!r}" if self.value else ""})" # pyright: ignore[reportAttributeAccessIssue]
    
    def __ne__(self, other) -> bool:
        if isinstance(other, TokenTypeEnum):
            return self.type != other
        if isinstance(other, Token):
            return self.type != other.type or self.value != other.value
        return NotImplemented
    
    def __eq__(self, other) -> bool:
        if isinstance(other, TokenTypeEnum):
            return self.type == other
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.type)

class Tokenizer:
    def __init__(self, source: str, conf: config.ConfigCls | None = None):
        self.conf = conf
        self.source = source
        self.src = source[:]
        self.tokens = []
        self.token_index = 0
        self.token_patterns = get_token_patterns()

    def _emit_token(self, match: str, token_type: TokenTypeEnum, include_match: bool = True) -> Token:
        self.src = self.src.lstrip(match)
        tok = Token(token_type, match if include_match else "")
        return tok

    def __iter__(self):
        return self

    def _lex_token(self) -> Token:
        if not self.src:
            return Token(InternalTokenType.EoF)
        
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
        
        # ^ Strings
        

        # ^ Everything else
        for token_pattern in self.token_patterns:
            if isinstance(token_pattern, RegExTokenPattern):
                if m := token_pattern.pattern.match(self.src):
                    return self._emit_token(
                        match = m.group(), 
                        token_type = token_pattern.associated_type
                    )
            elif isinstance(token_pattern, StringTokenPattern):
                if self.src.startswith(token_pattern.pattern):
                    return self._emit_token(
                        match = token_pattern.pattern, 
                        token_type = token_pattern.associated_type
                    )
        else:
            raise errors.SyntaxError(f"Invalid character found: U+{ord(self.src):x}")

    def peek(self, offset: int = 0) -> Token:
        while self.token_index + offset >= len(self.tokens):
            tok = self._lex_token()
            if tok.type == InternalTokenType._IgnoreByTokenizer:
                continue
            self.tokens.append(tok)
            if tok.type == InternalTokenType.EoF:
                break
        return self.tokens[self.token_index + offset]
    
    def advance(self, tok_types: TokenTypeSequence | None = None, error: errors.BaseSapphireError | None = None) -> Token:
        
        tok = self.peek()
        if tok_types is None: 
            tok_types = tuple()
        if isinstance(tok_types, TokenTypeEnum):
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
        if isinstance(tok_types, TokenTypeEnum):
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
        while self.peek().type != InternalTokenType.EoF:
            self.advance()
        return self.tokens