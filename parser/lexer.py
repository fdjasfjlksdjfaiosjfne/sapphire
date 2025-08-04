import typing

from parser._lexer.lexer import Tokenizer, Token
from parser._lexer.meta_token_types import main
main() # ? Writing the token_types file first...
del main # We're done with this.
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