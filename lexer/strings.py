from __future__ import annotations
from backend import errors
from backend.config.dataclass import RootConfigCls
from lexer.token_types import TokenTypeEnum
from lexer.internal_token_types import InternalTokenType, ITTTypeChecking
from lexer.data.patterns import IDENTIFIER_REGEX

class Token:
    
    def __init__(self, 
                 type: TokenTypeEnum | ITTTypeChecking, 
                 value: str = "" # This won't always be an string, it's just the most common occurence by FAR
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

class StringSubLexer:
    conf: RootConfigCls
    def _format_str(self) -> InterpolatedStrToken | None:
        for start in self._get_interpolated_str_start():
            if self.src.startswith(start):
                location = self.src.find(start[-1], 0, len(start)+1)
                prefixes = self.src[:location]
                quote = self.src[location:]
                self.src.removeprefix(start)
                return self._parse_format_str_content(prefixes, quote)
        return None

    def _parse_format_str_content(self, prefixes, quote) -> InterpolatedStrToken:
        ls = []
        def append(i):
            if isinstance(i, str) and isinstance(ls[-1], str):
                ls[-1] += i
            ls.append(i)
        
        interpolation = self.conf.customization.literals.strings.interpolation
        bracket_escape_method = interpolation.bracket_escape_method
        while self.src.startswith(quote):
            # ^ Any backslash escape
            if self.src.startswith("\\"):
                append(self.src[:2])
                self.src = self.src[2:]
            
            # ^ Escaped stuff
            elif (bracket_escape_method.opening.get() == "double"
                  and self.src.startswith(interpolation.expression_syntax.start.get()[0] * 2)):
                le = len(interpolation.expression_syntax.start.get()[0] * 2)
                append(self.src[:le])
                self.src = self.src[le:]
            elif (bracket_escape_method.closing.get() == "double"
                  and self.src.startswith(interpolation.expression_syntax.end.get()[0] * 2)):
                le = len(interpolation.expression_syntax.end.get()[0] * 2)
                append(self.src[:le])
                self.src = self.src[le:]

            # ^ Un-escaped brackets
            elif self.src.startswith(interpolation.expression_syntax.start.get()):
                append(self._parse_expr_format_str())
            # ^ Identifier syntax
            elif (interpolation.allow_identifier_syntax.get()
                  and self.src.startswith(interpolation.identifier_prefix_syntax.get())):
                match = IDENTIFIER_REGEX.match(self.src[1:])
                if match:
                    match.group()
        return InterpolatedStrToken(prefixes, ls)

    def _get_interpolated_str_start(self) -> list[str]:
        strs = self.conf.customization.literals.strings
        accessibility = strs.interpolation.accessibility.get()
        str_formats = strs.get_all_possible_starts()
        if accessibility == "never":
            return []
        elif accessibility == "always":
            return str_formats
        elif accessibility == "disable_by_prefix":
            _ = []
            for i in str_formats:
                if strs.interpolation.prefix_syntax.get() not in i:
                    _.append(i)
        elif accessibility == "enable_by_prefix":
            _ = []
            for i in str_formats:
                if strs.interpolation.prefix_syntax.get() in i:
                    _.append(i)
        elif accessibility == "disable_by_delimeter":
            _ = []
            for i in str_formats:
                for j in strs.interpolation.prefix_syntax.get():
                    if j not in i:
                        _.append(i)
        elif accessibility == "enable_by_delimeter":
            _ = []
            for i in str_formats:
                for j in strs.interpolation.prefix_syntax.get():
                    if j in i:
                        _.append(i)
        else:
            raise errors.InternalError
        return _

    def _parse_expr_format_str(self):
        pass
