import pytest
import sys
from pprint import pprint

sys.path.insert(0, r"C:\Users\Tien Dung\Dropbox\Script\Sapphire Family\Sapphire")

from parser.lexer._lexer_lexer import Tokenizer, Token, TokenType

@pytest.mark.parametrize("src,expected", [
    ("1 + 2", [
        Token(TokenType.PV_Int, "1"),
        Token(TokenType.BINOP_Addition),
        Token(TokenType.PV_Int, "2"),
        Token(TokenType.EoF)
    ]),
    ("print('Hello World!')", [
        Token(TokenType.Identifier, "print"),
        Token(TokenType.PR_OpenParenthesis),
        Token(TokenType.PV_String, "'Hello World!'"),
        Token(TokenType.PR_CloseParenthesis),
        Token(TokenType.EoF)
    ]),
    ("sapphire_root = Path(__file__).resolve().parent.parent.parent", [
        Token(TokenType.Identifier, "sapphire_root"),
        Token(TokenType.AssignOper),
        Token(TokenType.Identifier, "Path"),
        Token(TokenType.PR_OpenParenthesis),
        Token(TokenType.Identifier, "__file__"),
        Token(TokenType.PR_CloseParenthesis),
        Token(TokenType.SYM_Dot),
        Token(TokenType.Identifier, "resolve"),
        Token(TokenType.PR_OpenParenthesis),
        Token(TokenType.PR_CloseParenthesis),
        Token(TokenType.SYM_Dot),
        Token(TokenType.Identifier, "parent"),
        Token(TokenType.SYM_Dot),
        Token(TokenType.Identifier, "parent"),
        Token(TokenType.SYM_Dot),
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