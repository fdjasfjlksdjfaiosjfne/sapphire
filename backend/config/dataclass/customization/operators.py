import typing
from dataclasses import dataclass

from backend.config.dataclass.bases import CustomDataclass, ConfOptWrapper as C, _UNFILLED

@dataclass(frozen=True, kw_only=True)
class AdditionOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["+"]] = C(_UNFILLED, "+")
    allow_string_concanentation: C[bool] = C(_UNFILLED, False)

@dataclass(frozen=True, kw_only=True)
class SubtractionOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["-"]] = C(_UNFILLED, "-")

@dataclass(frozen=True, kw_only=True)
class MultiplicationOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["*"]] = C(_UNFILLED, "*")

@dataclass(frozen=True, kw_only=True)
class TrueDivisionOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["/"]] = C(_UNFILLED, "/")

@dataclass(frozen=True, kw_only=True)
class FloorDivisionOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["//", "div"]] = C(_UNFILLED, "//")

@dataclass(frozen=True, kw_only=True)
class ModulusOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["%", "mod"]] = C(_UNFILLED, "%")

@dataclass(frozen=True, kw_only=True)
class ExponentationOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["**", "^", "exp", "pow"]] = C(_UNFILLED, "**")

@dataclass(frozen=True, kw_only=True)
class ArithmeticOperatorsConfigCls(CustomDataclass):
    addition: AdditionOperatorConfigCls = AdditionOperatorConfigCls()
    subtraction: SubtractionOperatorConfigCls = SubtractionOperatorConfigCls()
    multiplication: MultiplicationOperatorConfigCls = MultiplicationOperatorConfigCls()
    true_division: TrueDivisionOperatorConfigCls = TrueDivisionOperatorConfigCls()
    floor_division: FloorDivisionOperatorConfigCls = FloorDivisionOperatorConfigCls()
    modulus: ModulusOperatorConfigCls = ModulusOperatorConfigCls()
    exponentiaion: ExponentationOperatorConfigCls = ExponentationOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class BinaryExclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["^^", "b^", "^", "xor"]] = C(_UNFILLED, "b^")

@dataclass(frozen=True, kw_only=True)
class BinaryInclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["||", "b|", "|", "ior", "or"]] = C(_UNFILLED, "b|")

@dataclass(frozen=True, kw_only=True)
class BinaryAndOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["&&", "b&", "&", "and"]] = C(_UNFILLED, "b&")

@dataclass(frozen=True, kw_only=True)
class BinaryOperatorsConfigCls(CustomDataclass):
    exclusive_or: BinaryExclusiveOrOperatorConfigCls = BinaryExclusiveOrOperatorConfigCls()
    inclusive_or: BinaryInclusiveOrOperatorConfigCls = BinaryInclusiveOrOperatorConfigCls()
    and_: BinaryAndOperatorConfigCls = BinaryAndOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class BooleanExclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["^^", "b^", "^", "xor"]] = C(_UNFILLED, "^")

@dataclass(frozen=True, kw_only=True)
class BooleanInclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["||", "b|", "|", "ior", "or"]] = C(_UNFILLED, "|")

@dataclass(frozen=True, kw_only=True)
class BooleanAndOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["&&", "b&", "&", "and"]] = C(_UNFILLED, "&")

@dataclass(frozen=True, kw_only=True)
class BooleanOperatorsConfigCls(CustomDataclass):
    exclusive_or: BooleanExclusiveOrOperatorConfigCls = BooleanExclusiveOrOperatorConfigCls()
    inclusive_or: BooleanInclusiveOrOperatorConfigCls = BooleanInclusiveOrOperatorConfigCls()
    and_: BooleanAndOperatorConfigCls = BooleanAndOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class LogicalExclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["^^", "^", "xor"]] = C(_UNFILLED, "xor")

@dataclass(frozen=True, kw_only=True)
class LogicalInclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["||", "|", "ior", "or"]] = C(_UNFILLED, "or")

@dataclass(frozen=True, kw_only=True)
class LogicalAndOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["&&", "&", "and"]] = C(_UNFILLED, "and")

@dataclass(frozen=True, kw_only=True)
class LogicalOperatorsConfigCls(CustomDataclass):
    exclusive_or: LogicalExclusiveOrOperatorConfigCls = LogicalExclusiveOrOperatorConfigCls()
    inclusive_or: LogicalInclusiveOrOperatorConfigCls = LogicalInclusiveOrOperatorConfigCls()
    and_: LogicalAndOperatorConfigCls = LogicalAndOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class EqualityOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["===", "=="]] = C(_UNFILLED, "==")

@dataclass(frozen=True, kw_only=True)
class InequalityOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["!==", "!=", "<>", "><"]] = C(_UNFILLED, "!=")

@dataclass(frozen=True, kw_only=True)
class LooseEqualityOperatorsConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    equality_syntax: C[typing.Literal["==", "~="]] = C(_UNFILLED, "~=")
    inequality_syntax: C[typing.Literal["~!=", "!~=", "!=", "~<>", "~><"]] = C(_UNFILLED, "!~=")

@dataclass(frozen=True, kw_only=True)
class SpaceshipOperatorConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["<=>", ">=<"]] = C(_UNFILLED, "<=>")

@dataclass(frozen=True, kw_only=True)
class ComparisonOperatorsConfigCls(CustomDataclass):
    equality: EqualityOperatorConfigCls = EqualityOperatorConfigCls()
    inequality: InequalityOperatorConfigCls = InequalityOperatorConfigCls()
    loose_equality: LooseEqualityOperatorsConfigCls = LooseEqualityOperatorsConfigCls()
    spaceship_operator: SpaceshipOperatorConfigCls = SpaceshipOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class StringConcanentationConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["..", "||"]] = C(_UNFILLED, "..")

@dataclass(frozen=True, kw_only=True)
class MatrixMultiplicationConfigCls(CustomDataclass):
    enabled: C[bool] = C(_UNFILLED, True)
    syntax: C[typing.Literal["@"]] = C(_UNFILLED, "@")

@dataclass(frozen=True, kw_only=True)
class OtherOperatorsConfigCls(CustomDataclass):
    string_concanentation: StringConcanentationConfigCls = StringConcanentationConfigCls()
    matrix_multiplication: MatrixMultiplicationConfigCls = MatrixMultiplicationConfigCls()

@dataclass(frozen=True, kw_only=True)
class OperatorsConfigCls(CustomDataclass):
    arithmetic: ArithmeticOperatorsConfigCls = ArithmeticOperatorsConfigCls()
    binary: BinaryOperatorsConfigCls = BinaryOperatorsConfigCls()
    booleans: BooleanOperatorsConfigCls = BooleanOperatorsConfigCls()
    comparison: ComparisonOperatorsConfigCls = ComparisonOperatorsConfigCls()
    logical: LogicalOperatorsConfigCls = LogicalOperatorsConfigCls()
    other: OtherOperatorsConfigCls = OtherOperatorsConfigCls()
    binary_expression_notation: C[typing.Literal["infix", "prefix", "postfix"]] = C(default = "infix")