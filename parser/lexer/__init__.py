import typing
from collections import abc

# Creating the files
from parser.lexer.meta import itt, token_types
itt.write_file()
token_types.write_file()

from parser.lexer.lexer import Tokenizer, Token
from parser.lexer.internal_token_types import *
from parser.lexer.token_types import *

TokenTypeSequence: typing.TypeAlias = (
    abc.Sequence[TokenTypeEnum]
    | abc.MutableSequence[TokenTypeEnum]
    | set[TokenTypeEnum]
    | abc.MutableSet[TokenTypeEnum]
    | TokenTypeEnum
)