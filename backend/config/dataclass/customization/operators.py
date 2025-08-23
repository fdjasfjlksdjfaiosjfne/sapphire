import typing
from dataclasses import dataclass

from backend.config.baseclasses import CustomDataclass, ConfigDescriptor, _UNFILLED

@dataclass(frozen=True, kw_only=True)
class AdditionOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["+"]] = ConfigDescriptor(_UNFILLED, "+")
    allow_string_concanentation: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, False)

@dataclass(frozen=True, kw_only=True)
class SubtractionOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["-"]] = ConfigDescriptor(_UNFILLED, "-")

@dataclass(frozen=True, kw_only=True)
class MultiplicationOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["*"]] = ConfigDescriptor(_UNFILLED, "*")

@dataclass(frozen=True, kw_only=True)
class TrueDivisionOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["/"]] = ConfigDescriptor(_UNFILLED, "/")

@dataclass(frozen=True, kw_only=True)
class FloorDivisionOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["//", "div"]] = ConfigDescriptor(_UNFILLED, "//")

@dataclass(frozen=True, kw_only=True)
class ModulusOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["%", "mod"]] = ConfigDescriptor(_UNFILLED, "%")

@dataclass(frozen=True, kw_only=True)
class ExponentationOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["**", "^", "exp", "pow"]] = ConfigDescriptor(_UNFILLED, "**")

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
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["^^", "b^", "^", "xor"]] = ConfigDescriptor(_UNFILLED, "b^")

@dataclass(frozen=True, kw_only=True)
class BinaryInclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["||", "b|", "|", "ior", "or"]] = ConfigDescriptor(_UNFILLED, "b|")

@dataclass(frozen=True, kw_only=True)
class BinaryAndOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["&&", "b&", "&", "and"]] = ConfigDescriptor(_UNFILLED, "b&")

@dataclass(frozen=True, kw_only=True)
class BinaryOperatorsConfigCls(CustomDataclass):
    exclusive_or: BinaryExclusiveOrOperatorConfigCls = BinaryExclusiveOrOperatorConfigCls()
    inclusive_or: BinaryInclusiveOrOperatorConfigCls = BinaryInclusiveOrOperatorConfigCls()
    and_: BinaryAndOperatorConfigCls = BinaryAndOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class BooleanExclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["^^", "b^", "^", "xor"]] = ConfigDescriptor(_UNFILLED, "^")

@dataclass(frozen=True, kw_only=True)
class BooleanInclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["||", "b|", "|", "ior", "or"]] = ConfigDescriptor(_UNFILLED, "|")

@dataclass(frozen=True, kw_only=True)
class BooleanAndOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["&&", "b&", "&", "and"]] = ConfigDescriptor(_UNFILLED, "&")

@dataclass(frozen=True, kw_only=True)
class BooleanOperatorsConfigCls(CustomDataclass):
    exclusive_or: BooleanExclusiveOrOperatorConfigCls = BooleanExclusiveOrOperatorConfigCls()
    inclusive_or: BooleanInclusiveOrOperatorConfigCls = BooleanInclusiveOrOperatorConfigCls()
    and_: BooleanAndOperatorConfigCls = BooleanAndOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class LogicalExclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["^^", "^", "xor"]] = ConfigDescriptor(_UNFILLED, "xor")

@dataclass(frozen=True, kw_only=True)
class LogicalInclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["||", "|", "ior", "or"]] = ConfigDescriptor(_UNFILLED, "or")

@dataclass(frozen=True, kw_only=True)
class LogicalAndOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["&&", "&", "and"]] = ConfigDescriptor(_UNFILLED, "and")

@dataclass(frozen=True, kw_only=True)
class LogicalOperatorsConfigCls(CustomDataclass):
    exclusive_or: LogicalExclusiveOrOperatorConfigCls = LogicalExclusiveOrOperatorConfigCls()
    inclusive_or: LogicalInclusiveOrOperatorConfigCls = LogicalInclusiveOrOperatorConfigCls()
    and_: LogicalAndOperatorConfigCls = LogicalAndOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class EqualityOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["===", "=="]] = ConfigDescriptor(_UNFILLED, "==")

@dataclass(frozen=True, kw_only=True)
class InequalityOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["!==", "!=", "<>", "><"]] = ConfigDescriptor(_UNFILLED, "!=")

@dataclass(frozen=True, kw_only=True)
class LooseEqualityOperatorsConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    equality_syntax: ConfigDescriptor[typing.Literal["==", "~="]] = ConfigDescriptor(_UNFILLED, "~=")
    inequality_syntax: ConfigDescriptor[typing.Literal["~!=", "!~=", "!=", "~<>", "~><"]] = ConfigDescriptor(_UNFILLED, "!~=")

@dataclass(frozen=True, kw_only=True)
class SpaceshipOperatorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["<=>", ">=<"]] = ConfigDescriptor(_UNFILLED, "<=>")

@dataclass(frozen=True, kw_only=True)
class ComparisonOperatorsConfigCls(CustomDataclass):
    equality: EqualityOperatorConfigCls = EqualityOperatorConfigCls()
    inequality: InequalityOperatorConfigCls = InequalityOperatorConfigCls()
    loose_equality: LooseEqualityOperatorsConfigCls = LooseEqualityOperatorsConfigCls()
    spaceship_operator: SpaceshipOperatorConfigCls = SpaceshipOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class StringConcanentationConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["..", "||"]] = ConfigDescriptor(_UNFILLED, "..")

@dataclass(frozen=True, kw_only=True)
class MatrixMultiplicationConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["@"]] = ConfigDescriptor(_UNFILLED, "@")

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