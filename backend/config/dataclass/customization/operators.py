import typing
from dataclasses import dataclass

from backend.config.baseclasses import custom_dataclass

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class AdditionOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["+"] = "+"
    allow_string_concanentation: bool = False

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class SubtractionOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["-"] = "-"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class MultiplicationOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["*"] = "*"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class TrueDivisionOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["/"] = "/"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class FloorDivisionOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["//", "div"] = "//"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ModulusOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["%", "mod"] = "%"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ExponentationOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["**", "^", "exp", "pow"] = "**"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ArithmeticOperatorsConfigCls:
    addition: AdditionOperatorConfigCls = AdditionOperatorConfigCls()
    subtraction: SubtractionOperatorConfigCls = SubtractionOperatorConfigCls()
    multiplication: MultiplicationOperatorConfigCls = MultiplicationOperatorConfigCls()
    true_division: TrueDivisionOperatorConfigCls = TrueDivisionOperatorConfigCls()
    floor_division: FloorDivisionOperatorConfigCls = FloorDivisionOperatorConfigCls()
    modulus: ModulusOperatorConfigCls = ModulusOperatorConfigCls()
    exponentiaion: ExponentationOperatorConfigCls = ExponentationOperatorConfigCls()

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class BinaryExclusiveOrOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["^^", "b^", "^", "xor"] = "b^"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class BinaryInclusiveOrOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["||", "b|", "|", "ior", "or"] = "b|"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class BinaryAndOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["&&", "b&", "&", "and"] = "b&"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class BinaryOperatorsConfigCls:
    exclusive_or: BinaryExclusiveOrOperatorConfigCls = BinaryExclusiveOrOperatorConfigCls()
    inclusive_or: BinaryInclusiveOrOperatorConfigCls = BinaryInclusiveOrOperatorConfigCls()
    and_: BinaryAndOperatorConfigCls = BinaryAndOperatorConfigCls()

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class BooleanExclusiveOrOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["^^", "b^", "^", "xor"] = "^"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class BooleanInclusiveOrOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["||", "b|", "|", "ior", "or"] = "|"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class BooleanAndOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["&&", "b&", "&", "and"] = "&"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class BooleanOperatorsConfigCls:
    exclusive_or: BooleanExclusiveOrOperatorConfigCls = BooleanExclusiveOrOperatorConfigCls()
    inclusive_or: BooleanInclusiveOrOperatorConfigCls = BooleanInclusiveOrOperatorConfigCls()
    and_: BooleanAndOperatorConfigCls = BooleanAndOperatorConfigCls()

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class LogicalExclusiveOrOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["^^", "^", "xor"] = "xor"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class LogicalInclusiveOrOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["||", "|", "ior", "or"] = "or"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class LogicalAndOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["&&", "&", "and"] = "and"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class LogicalOperatorsConfigCls:
    exclusive_or: LogicalExclusiveOrOperatorConfigCls = LogicalExclusiveOrOperatorConfigCls()
    inclusive_or: LogicalInclusiveOrOperatorConfigCls = LogicalInclusiveOrOperatorConfigCls()
    and_: LogicalAndOperatorConfigCls = LogicalAndOperatorConfigCls()

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class EqualityOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["===", "=="] = "=="

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class InequalityOperatorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["!==", "!=", "<>", "><"] = "!="

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class LooseEqualityOperatorsConfigCls:
    enabled: bool = True
    equality_syntax: typing.Literal["==", "~="] = "~="
    inequality_syntax: typing.Literal["~!=", "!~=",
                                      "!=", "~<>",
                                      "~><"] = "!~="

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ComparisonOperatorsConfigCls:
    equality: EqualityOperatorConfigCls = EqualityOperatorConfigCls()
    inequality: InequalityOperatorConfigCls = InequalityOperatorConfigCls()
    loose_equality: LooseEqualityOperatorsConfigCls = LooseEqualityOperatorsConfigCls()

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class StringConcanentationConfigCls:
    enabled: bool = True
    syntax: typing.Literal["..", "||"] = ".."

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class MatrixMultiplicationConfigCls:
    enabled: bool = True
    syntax: typing.Literal["@"] = "@"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class OtherOperatorsConfigCls:
    string_concanentation: StringConcanentationConfigCls = StringConcanentationConfigCls()
    matrix_multiplication: MatrixMultiplicationConfigCls = MatrixMultiplicationConfigCls()

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class OperatorsConfigCls:
    arithmetic: ArithmeticOperatorsConfigCls = ArithmeticOperatorsConfigCls()
    binary: BinaryOperatorsConfigCls = BinaryOperatorsConfigCls()
    booleans: BooleanOperatorsConfigCls = BooleanOperatorsConfigCls()
    comparison: ComparisonOperatorsConfigCls = ComparisonOperatorsConfigCls()
    logical: LogicalOperatorsConfigCls = LogicalOperatorsConfigCls()
    other: OtherOperatorsConfigCls = OtherOperatorsConfigCls()