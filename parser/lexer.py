import typing

# Creating the files
from parser._lexer.meta import itt, token_types
itt.write_file()
token_types.write_file()

from parser._lexer.lexer import Tokenizer, Token
from parser._lexer.internal_token_types import *
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