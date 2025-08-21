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
    addition: ConfigDescriptor[AdditionOperatorConfigCls] = ConfigDescriptor(_UNFILLED, AdditionOperatorConfigCls())
    subtraction: ConfigDescriptor[SubtractionOperatorConfigCls] = ConfigDescriptor(_UNFILLED, SubtractionOperatorConfigCls())
    multiplication: ConfigDescriptor[MultiplicationOperatorConfigCls] = ConfigDescriptor(_UNFILLED, MultiplicationOperatorConfigCls())
    true_division: ConfigDescriptor[TrueDivisionOperatorConfigCls] = ConfigDescriptor(_UNFILLED, TrueDivisionOperatorConfigCls())
    floor_division: ConfigDescriptor[FloorDivisionOperatorConfigCls] = ConfigDescriptor(_UNFILLED, FloorDivisionOperatorConfigCls())
    modulus: ConfigDescriptor[ModulusOperatorConfigCls] = ConfigDescriptor(_UNFILLED, ModulusOperatorConfigCls())
    exponentiaion: ConfigDescriptor[ExponentationOperatorConfigCls] = ConfigDescriptor(_UNFILLED, ExponentationOperatorConfigCls())

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
    exclusive_or: ConfigDescriptor[BinaryExclusiveOrOperatorConfigCls] = ConfigDescriptor(_UNFILLED, BinaryExclusiveOrOperatorConfigCls())
    inclusive_or: ConfigDescriptor[BinaryInclusiveOrOperatorConfigCls] = ConfigDescriptor(_UNFILLED, BinaryInclusiveOrOperatorConfigCls())
    and_: ConfigDescriptor[BinaryAndOperatorConfigCls] = ConfigDescriptor(_UNFILLED, BinaryAndOperatorConfigCls())

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
    exclusive_or: ConfigDescriptor[BooleanExclusiveOrOperatorConfigCls] = ConfigDescriptor(_UNFILLED, BooleanExclusiveOrOperatorConfigCls())
    inclusive_or: ConfigDescriptor[BooleanInclusiveOrOperatorConfigCls] = ConfigDescriptor(_UNFILLED, BooleanInclusiveOrOperatorConfigCls())
    and_: ConfigDescriptor[BooleanAndOperatorConfigCls] = ConfigDescriptor(_UNFILLED, BooleanAndOperatorConfigCls())

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
    exclusive_or: ConfigDescriptor[LogicalExclusiveOrOperatorConfigCls] = ConfigDescriptor(_UNFILLED, LogicalExclusiveOrOperatorConfigCls())
    inclusive_or: ConfigDescriptor[LogicalInclusiveOrOperatorConfigCls] = ConfigDescriptor(_UNFILLED, LogicalInclusiveOrOperatorConfigCls())
    and_: ConfigDescriptor[LogicalAndOperatorConfigCls] = ConfigDescriptor(_UNFILLED, LogicalAndOperatorConfigCls())

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
    equality: ConfigDescriptor[EqualityOperatorConfigCls] = ConfigDescriptor(_UNFILLED, EqualityOperatorConfigCls())
    inequality: ConfigDescriptor[InequalityOperatorConfigCls] = ConfigDescriptor(_UNFILLED, InequalityOperatorConfigCls())
    loose_equality: ConfigDescriptor[LooseEqualityOperatorsConfigCls] = ConfigDescriptor(_UNFILLED, LooseEqualityOperatorsConfigCls())
    spaceship_operator: ConfigDescriptor[SpaceshipOperatorConfigCls] = ConfigDescriptor(_UNFILLED, SpaceshipOperatorConfigCls())

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
    string_concanentation: ConfigDescriptor[StringConcanentationConfigCls] = ConfigDescriptor(_UNFILLED, StringConcanentationConfigCls())
    matrix_multiplication: ConfigDescriptor[MatrixMultiplicationConfigCls] = ConfigDescriptor(_UNFILLED, MatrixMultiplicationConfigCls())

@dataclass(frozen=True, kw_only=True)
class OperatorsConfigCls(CustomDataclass):
    arithmetic: ConfigDescriptor[ArithmeticOperatorsConfigCls] = ConfigDescriptor(_UNFILLED, ArithmeticOperatorsConfigCls())
    binary: ConfigDescriptor[BinaryOperatorsConfigCls] = ConfigDescriptor(_UNFILLED, BinaryOperatorsConfigCls())
    booleans: ConfigDescriptor[BooleanOperatorsConfigCls] = ConfigDescriptor(_UNFILLED, BooleanOperatorsConfigCls())
    comparison: ConfigDescriptor[ComparisonOperatorsConfigCls] = ConfigDescriptor(_UNFILLED, ComparisonOperatorsConfigCls())
    logical: ConfigDescriptor[LogicalOperatorsConfigCls] = ConfigDescriptor(_UNFILLED, LogicalOperatorsConfigCls())
    other: ConfigDescriptor[OtherOperatorsConfigCls] = ConfigDescriptor(_UNFILLED, OtherOperatorsConfigCls())