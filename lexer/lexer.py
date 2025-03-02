import sys; sys.dont_write_bytecode = True
from typing import *
from .tokens import *
import regex as re

class _TokenizeReturnValue_(TypedDict):
    tokens: List[Token]
    directives: List[Directive]

class Lexer:
    def __init__(self):
        self.tokens: List[Token] = []
        self.directives: List[Directive] = []
    
    def tokenize(self, src: str) -> _TokenizeReturnValue_:
        self.src = src
        self.tokens = []
        while self.src:
            # ? Stuff that should be at the start of a line
            if self.last_token.type == TokenType.NewLine:
                # > Decorators
                if match := re.match(f"@[{regex_patterns[TokenType.Identifier]}]"): 
                    self.snap(match.group(), TokenType.Decorator)
                
                # > Labels
                elif match := re.match(f"{regex_patterns[TokenType.Identifier]}:"): 
                    self.snap(match.group(), TokenType.Label)
                
                # > Directives
                elif match := re.match(f"#{regex_patterns[TokenType.Identifier]}"):
                    self.parse_directives()
            # > Comments
            elif (match := compile("//.*").match(self.src)) or (match := compile(r"/\*[.\s]*(\*/)?").match(self.src)):
                self.src = self.src[len(match):]
            # > Everything else
            else:
                for token_type, dict_ in regex_patterns.items():
                    for pattern in dict_["patterns"]:
                        if match := pattern.match(self.src):
                            self.snap(match.group(), token_type, dict_.get("include_value", True))
                else: break
        self.tokens.append(Token(TokenType.EoF))
        return {"tokens": self.tokens, "directives": self.directives}
    
    def parse_directives(self):
        self.tokens
    
    def snap(self, match, token_type: TokenType, include_match: bool = True) -> NoReturn:
        self.src = self.src[len(match):]
        self.tokens.append(Token(token_type, match if include_match else None))
    
    @property
    def last_token(self) -> Token: return self.tokens[-1] if self.tokens else Token(TokenType.NOTHING)