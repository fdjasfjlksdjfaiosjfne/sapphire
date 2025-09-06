from __future__ import annotations
from backend import errors
from backend.config import RootConfigCls, StringLiteralsConfigCls
from lexer.token_types import TokenTypeEnum
from lexer.internal_token_types import InternalTokenType, ITTTypeChecking
from lexer.data.patterns import IDENTIFIER_REGEX
class StringSubLexer:
    _str_conf: StringLiteralsConfigCls
    src: str
    def _parse_str(self) -> InterpolatedStrToken | None:
        for start in self._str_conf.get_all_possible_starts():
            if self.src.startswith(start):
                location = self.src.find(start[-1], 0, len(start)+1)
                prefixes = self.src[:location]
                quote = self.src[location:]
                self.src.removeprefix(start)
                return self._parse_format_str_content(prefixes, quote)
        return None

    def _parse_format_str_content(self, prefixes: str, quote: str) -> InterpolatedStrToken:
        ls = []
        def append(i):
            if isinstance(i, str) and isinstance(ls[-1], str):
                ls[-1] += i
            ls.append(i)
        
        interpolation = self._str_conf.interpolation
        while self.src.startswith(quote):
            

            # ^ Un-escaped brackets
            if self.src.startswith(interpolation.expression_syntax.start.get()):
                append(self._parse_expr_format_str())
            # ^ Identifier syntax
            elif (interpolation.allow_identifier_syntax.get()
                  and self.src.startswith(interpolation.identifier_prefix_syntax.get())):
                match = IDENTIFIER_REGEX.match(self.src[1:])
                if match:
                    match.group()
        return InterpolatedStrToken(prefixes, ls)
    
    def _parse_expr_format_str(self):
        pass

class Token:
    def __init__(self, 
                 type: TokenTypeEnum | ITTTypeChecking, 
                 value: str = ""
                 ):
        self.type = type
        self.value = value

    def __str__(self) -> str: return repr(self)

    def __repr__(self) -> str:
        return f"Token(type={self.type.name}{f", value={self.value!r}" if self.value else ""})" # pyright: ignore[reportAttributeAccessIssue]
    
    def __ne__(self, other) -> bool:
        if isinstance(other, (TokenTypeEnum, ITTTypeChecking)):
            return self.type != other
        if isinstance(other, Token):
            return self.type != other.type or self.value != other.value
        return NotImplemented
    
    def __eq__(self, other) -> bool:
        if isinstance(other, (TokenTypeEnum, ITTTypeChecking)):
            return self.type == other
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.type)

class InterpolatedStrToken(Token):
    def __init__(self, prefixes: str, ls: list[str | FormattedValue]):
        self.type = InternalTokenType.Primitives.String
        self.prefixes = prefixes
        self.ls = ls
        self.value = ""

class FormattedValue:
    def __init__(self, value, 
                 conversion: int, 
                 formatting: InterpolatedStrToken | None = None):
        self.value = value
        self.conversion = conversion
        self.formatting = formatting