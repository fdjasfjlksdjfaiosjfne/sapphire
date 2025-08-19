import typing
from dataclasses import dataclass

from backend.config.baseclasses import CustomDataclass

@dataclass(frozen=True, kw_only=True)
class AdditionOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["+"] = "+"
    allow_string_concanentation: bool = False

@dataclass(frozen=True, kw_only=True)
class SubtractionOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["-"] = "-"

@dataclass(frozen=True, kw_only=True)
class MultiplicationOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["*"] = "*"

@dataclass(frozen=True, kw_only=True)
class TrueDivisionOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["/"] = "/"

@dataclass(frozen=True, kw_only=True)
class FloorDivisionOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["//", "div"] = "//"

@dataclass(frozen=True, kw_only=True)
class ModulusOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["%", "mod"] = "%"

@dataclass(frozen=True, kw_only=True)
class ExponentationOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["**", "^", "exp", "pow"] = "**"

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
    enabled: bool = True
    syntax: typing.Literal["^^", "b^", "^", "xor"] = "b^"

@dataclass(frozen=True, kw_only=True)
class BinaryInclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["||", "b|", "|", "ior", "or"] = "b|"

@dataclass(frozen=True, kw_only=True)
class BinaryAndOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["&&", "b&", "&", "and"] = "b&"

@dataclass(frozen=True, kw_only=True)
class BinaryOperatorsConfigCls(CustomDataclass):
    exclusive_or: BinaryExclusiveOrOperatorConfigCls = BinaryExclusiveOrOperatorConfigCls()
    inclusive_or: BinaryInclusiveOrOperatorConfigCls = BinaryInclusiveOrOperatorConfigCls()
    and_: BinaryAndOperatorConfigCls = BinaryAndOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class BooleanExclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["^^", "b^", "^", "xor"] = "^"

@dataclass(frozen=True, kw_only=True)
class BooleanInclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["||", "b|", "|", "ior", "or"] = "|"

@dataclass(frozen=True, kw_only=True)
class BooleanAndOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["&&", "b&", "&", "and"] = "&"

@dataclass(frozen=True, kw_only=True)
class BooleanOperatorsConfigCls(CustomDataclass):
    exclusive_or: BooleanExclusiveOrOperatorConfigCls = BooleanExclusiveOrOperatorConfigCls()
    inclusive_or: BooleanInclusiveOrOperatorConfigCls = BooleanInclusiveOrOperatorConfigCls()
    and_: BooleanAndOperatorConfigCls = BooleanAndOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class LogicalExclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["^^", "^", "xor"] = "xor"

@dataclass(frozen=True, kw_only=True)
class LogicalInclusiveOrOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["||", "|", "ior", "or"] = "or"

@dataclass(frozen=True, kw_only=True)
class LogicalAndOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["&&", "&", "and"] = "and"

@dataclass(frozen=True, kw_only=True)
class LogicalOperatorsConfigCls(CustomDataclass):
    exclusive_or: LogicalExclusiveOrOperatorConfigCls = LogicalExclusiveOrOperatorConfigCls()
    inclusive_or: LogicalInclusiveOrOperatorConfigCls = LogicalInclusiveOrOperatorConfigCls()
    and_: LogicalAndOperatorConfigCls = LogicalAndOperatorConfigCls()

@dataclass(frozen=True, kw_only=True)
class EqualityOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["===", "=="] = "=="

@dataclass(frozen=True, kw_only=True)
class InequalityOperatorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["!==", "!=", "<>", "><"] = "!="

@dataclass(frozen=True, kw_only=True)
class LooseEqualityOperatorsConfigCls(CustomDataclass):
    enabled: bool = True
    equality_syntax: typing.Literal["==", "~="] = "~="
    inequality_syntax: typing.Literal["~!=", "!~=",
                                      "!=", "~<>",
                                      "~><"] = "!~="

@dataclass(frozen=True, kw_only=True)
class ComparisonOperatorsConfigCls(CustomDataclass):
    equality: EqualityOperatorConfigCls = EqualityOperatorConfigCls()
    inequality: InequalityOperatorConfigCls = InequalityOperatorConfigCls()
    loose_equality: LooseEqualityOperatorsConfigCls = LooseEqualityOperatorsConfigCls()

@dataclass(frozen=True, kw_only=True)
class StringConcanentationConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["..", "||"] = ".."

@dataclass(frozen=True, kw_only=True)
class MatrixMultiplicationConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["@"] = "@"

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