import pytest
import sys
sys.path.insert(0, r"C:\Users\Tien Dung\Dropbox\Script\Sapphire Family\Sapphire")
from parser.parser import Parser
from backend import errors
from parser.lexer._lexer_lexer import TokenType, Token
from parser import nodes as Nodes

@pytest.mark.parametrize("src,expected", [
    ("1 + 2", Nodes.ModuleNode(
        Nodes.CodeBlockNode([
            Nodes.BinaryNode(
            left = Nodes.IntNode(1),
            oper = TokenType.BINOP_Addition,
            right = Nodes.IntNode(2)
            )
        ])
    )),
    ("3 + 24.37 * foo", Nodes.ModuleNode(
        Nodes.CodeBlockNode([
            Nodes.BinaryNode(
                left = Nodes.IntNode(3),
                oper = TokenType.BINOP_Addition,
                right = Nodes.BinaryNode(
                    left = Nodes.FloatNode(24.37),
                    oper = TokenType.BINOP_Multiplication,
                    right = Nodes.IdentifierNode("foo")
                )
            )
        ])
    )),
    ("1 +", errors.SyntaxError)
])
def test_parser(src: str, expected: type[errors.SapphireError] | Nodes.BaseASTNode):
    p = Parser(src)
    if isinstance(expected, type) and issubclass(expected, errors.SapphireError):
        with pytest.raises(expected):
            p.parse_module()
    else:
        assert p.parse_module() == expected