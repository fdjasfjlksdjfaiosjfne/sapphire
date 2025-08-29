import pytest

from backend import errors
from parser.lexer import Tokenizer, Token, TokenType

@pytest.mark.parametrize("src,expected", [
    ("1 + 2", [
        Token(TokenType.Primitives.Int, "1"),
        Token(TokenType.Operators.Binary.Addition),
        Token(TokenType.Primitives.Int, "2"),
        Token(TokenType.EoF)
    ]),
    ("print('Hello World!')", [
        Token(TokenType.Identifier, "print"),
        Token(TokenType.Parentheses.OpenParenthesis),
        Token(TokenType.Primitives.String, "'Hello World!'"),
        Token(TokenType.Parentheses.CloseParenthesis),
        Token(TokenType.EoF)
    ]),
    ("sapphire_root = Path(__file__).resolve().parent.parent.parent", [
        Token(TokenType.Identifier, "sapphire_root"),
        Token(TokenType.Symbols.AssignOper),
        Token(TokenType.Identifier, "Path"),
        Token(TokenType.Parentheses.OpenParenthesis),
        Token(TokenType.Identifier, "__file__"),
        Token(TokenType.Parentheses.CloseParenthesis),
        Token(TokenType.Symbols.AttributeAccess),
        Token(TokenType.Identifier, "resolve"),
        Token(TokenType.Parentheses.OpenParenthesis),
        Token(TokenType.Parentheses.CloseParenthesis),
        Token(TokenType.Symbols.AttributeAccess),
        Token(TokenType.Identifier, "parent"),
        Token(TokenType.Symbols.AttributeAccess),
        Token(TokenType.Identifier, "parent"),
        Token(TokenType.Symbols.AttributeAccess),
        Token(TokenType.Identifier, "parent"),
        Token(TokenType.EoF)
    ]),
])
def test_token_stream(src: str, expected: list[Token]):
    t = Tokenizer(src)
    toks = t.dump_all()
    assert len(toks) == len(expected)
    for e, r in zip(expected, toks):
        assert e.type == r.type
        assert r.value == r.value