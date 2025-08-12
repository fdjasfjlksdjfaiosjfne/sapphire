import typing

from parser._lexer.lexer import Tokenizer, Token
from parser._lexer.meta.token_types import write_file
write_file() # ? Writing the token_types file first...
del write_file # Alright, we're done with this.
from parser._lexer.token_types import *

TokenTypeSequence: typing.TypeAlias = (
    typing.Union [
        typing.Sequence[TokenTypeEnum],
        typing.MutableSequence[TokenTypeEnum],
        set[TokenTypeEnum],
        typing.MutableSet[TokenTypeEnum],
        TokenTypeEnum
    ]
)