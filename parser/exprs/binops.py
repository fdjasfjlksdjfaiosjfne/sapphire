from __future__ import annotations
import typing
import jsonschema

from backend import errors
from backend.config import CONFIG
from lexer import BinaryOperators, TokenTypeEnum, TokenTypeSequence
from parser.core import ParserNamespaceSkeleton
import parser.nodes as Nodes

BINARY_NODE_DICT = {
    "logical_xor": BinaryOperators.LogicalXor,
    "logical_or": BinaryOperators.LogicalOr,
    "logical_and": BinaryOperators.LogicalAnd,
    "hybrid_xor": BinaryOperators.HybridXor,
    "hybrid_or": BinaryOperators.HybridOr,
    "hybrid_and": BinaryOperators.HybridAnd,
    "binary_xor": BinaryOperators.BinaryXor,
    "binary_or": BinaryOperators.BinaryOr,
    "binary_and": BinaryOperators.BinaryAnd,
    "spaceship": BinaryOperators.Spaceship,
    "containing": [BinaryOperators.Containing, BinaryOperators.NotContaining],
    "identity": [BinaryOperators.Identity, BinaryOperators.NotIdentity],
    "comparison": [BinaryOperators.LessThanOrEqualTo, BinaryOperators.LessThan,
                   BinaryOperators.Equality, BinaryOperators.Inequality,
                   BinaryOperators.GreaterThanOrEqualTo, BinaryOperators.GreaterThan],
    "additive": [BinaryOperators.Addition, BinaryOperators.Subtraction],
    "multiplicative": [BinaryOperators.Multiplication, BinaryOperators.MatrixMultiplication,
                       BinaryOperators.TrueDivision, BinaryOperators.FloorDivision],
    "exponentiative": BinaryOperators.Exponentiation
}

BINARY_NODE_DICT["full"] = []
for v in BINARY_NODE_DICT.values():
    if isinstance(v, TokenTypeEnum):
        BINARY_NODE_DICT["full"].append(v)
    else:
        BINARY_NODE_DICT["full"].extend(v)

# TODO: Make a dynamic system that allows for custom operator ordering
class InfixBinaryOperations(ParserNamespaceSkeleton):
    def _binary_parser_factory(self, operator_tokens: TokenTypeSequence,
                               next_in_precendence: typing.Callable[[], Nodes.ExprNode],
                               **context):
        operator_tokens = self._to_token_sequence(operator_tokens)
        
        def method(lhs: Nodes.ExprNode | None = None) -> (Nodes.BinaryNode | Nodes.ExprNode):
                    lhs = next_in_precendence(**context)
                    if self._peek() in operator_tokens:
                        return Nodes.BinaryNode(
                            left = lhs,
                            oper = self._advance().type,
                            right = method(**context)
                        )
                    return lhs
        return method

    def _parse_binary_node_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._parse_logical_xor_expr(**context)

    def _parse_logical_xor_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["logical_xor"],
            next_in_precendence = self._parse_logical_or_expr
        )(**context)
    
    def _parse_logical_or_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["logical_or"],
            next_in_precendence = self._parse_logical_and_expr
        )(**context)

    def _parse_logical_and_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["logical_and"],
            next_in_precendence = self._parse_hybrid_xor_expr
        )(**context)

    def _parse_hybrid_xor_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["hybrid_xor"],
            next_in_precendence = self._parse_hybrid_or_expr
        )(**context)
    
    def _parse_hybrid_or_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["hybrid_or"],
            next_in_precendence = self._parse_hybrid_and_expr
        )(**context)

    def _parse_hybrid_and_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["hybrid_and"],
            next_in_precendence = self._parse_binary_xor_expr
        )(**context)

    def _parse_binary_xor_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BinaryOperators.BinaryXor,
            next_in_precendence = self._parse_binary_or_expr
        )(**context)
    
    def _parse_binary_or_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BinaryOperators.BinaryOr,
            next_in_precendence = self._parse_binary_and_expr
        )(**context)

    def _parse_binary_and_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BinaryOperators.BinaryAnd,
            next_in_precendence = self._parse_spaceship_expr
        )(**context)
    
    def _parse_spaceship_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["spaceship"],
            next_in_precendence = self._parse_containing_expr
        )(**context)
    
    def _parse_containing_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["containing"],
            next_in_precendence = self._parse_comparison_expr
        )(**context)

    def _parse_comparison_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["comparison"],
            next_in_precendence = self._parse_additive_expr
        )(**context)

    def _parse_additive_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["additive"],
            next_in_precendence = self._parse_multiplicative_expr
        )(**context)
    
    def _parse_multiplicative_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["multiplicative"],
            next_in_precendence = self._parse_exponentiative_expr
        )(**context)

    def _parse_exponentiative_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        return self._binary_parser_factory(
            operator_tokens = BINARY_NODE_DICT["exponentiative"],
            next_in_precendence = self._parse_unary_expr
        )(**context)

class PrefixBinaryOperations(ParserNamespaceSkeleton):
    def _parse_binary_node_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        raise errors.InProgress

class PostfixBinaryOperations(ParserNamespaceSkeleton):
    def _parse_binary_node_expr(self, **context) -> Nodes.BinaryNode | Nodes.ExprNode:
        raise errors.InProgress


match CONFIG.customization.operators.binary_expression_notation.get():
    case "infix":
        BinaryOperations = InfixBinaryOperations
    case "prefix":
        BinaryOperations = PrefixBinaryOperations
    case "postfix":
        BinaryOperations = PostfixBinaryOperations
    case c:
        typing.assert_never(c)