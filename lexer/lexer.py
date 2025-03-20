from typing import List
from .tokens import Token, regex_patterns, TokenType
import regex as re


class Lexer:
    # @enforce_types
    
    # @enforce_types
    @classmethod
    def tokenize(cls, src: str) -> List[Token]:
        cls.src = src
        cls.tokens = []
        while cls.src:
            # ? Stuff that should be at the start of a line
            if cls.last_token() == TokenType.NewLine:
                # > Decorators
                if match := re.match(f"@[{regex_patterns[TokenType.Identifier]}]"): 
                    cls.snap(match.group(), TokenType.Decorator)
                
                # > Labels
                elif match := re.match(f"{regex_patterns[TokenType.Identifier]}:"): 
                    cls.snap(match.group(), TokenType.Label)
            # ? Everything else
            else:
                for token_type, dict_ in regex_patterns.items():
                    for pattern in dict_["patterns"]:
                        if match := pattern.match(cls.src):
                            cls.snap(match.group(), token_type, dict_.get("include_value", False))
                            break
                    else:
                        continue
                    break
                    
                else:
                    raise Exception("Unregconized character")
        cls.tokens = [token for token in cls.tokens if token != TokenType.NOTHING]
        cls.tokens.append(Token(TokenType.EoF))
        # Dispose
        tkns = cls.tokens
        del cls.src, cls.tokens
        return tkns
    
    @classmethod
    def snap(cls, match, token_type: TokenType, include_match: bool = True) -> None:
        cls.src = cls.src[len(match):]
        cls.tokens.append(Token(token_type, match if include_match else None))
    
    @classmethod
    def last_token(cls) -> Token: return cls.tokens[-1] if cls.tokens else Token(TokenType.NOTHING)