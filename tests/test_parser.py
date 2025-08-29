import pytest

from parser.parser import Parser
from backend import errors
from parser.lexer import TokenType, Token, BinaryOperators
from parser import nodes as Nodes


@pytest.mark.parametrize("src,expected", [
    ("1 + 2", Nodes.ModuleNode(
        Nodes.CodeBlockNode([
            Nodes.BinaryNode(
            left = Nodes.IntNode(1),
            oper = TokenType.Operators.Binary.Addition,
            right = Nodes.IntNode(2)
            )
        ])
    )),
    ("3 + 24.37 * foo", Nodes.ModuleNode(
        Nodes.CodeBlockNode([
            Nodes.BinaryNode(
                left = Nodes.IntNode(3),
                oper = TokenType.Operators.Binary.Addition,
                right = Nodes.BinaryNode(
                    left = Nodes.FloatNode(24.37),
                    oper = TokenType.Operators.Binary.Multiplication,
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