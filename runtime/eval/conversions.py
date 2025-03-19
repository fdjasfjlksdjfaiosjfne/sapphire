from parser.nodes import *
from runtime.values import *
from lexer.tokens import TokenType

def bool(value: RuntimeVal) -> BoolVal | NotImplementedVal:
    match value:
        case ValueType.Bool: 
            return value
        case ValueType.Int | ValueType.Float:
            return BoolVal(False) if value == 0 else BoolVal(True)
        case ValueType.Str:
            return BoolVal(False) if value == "" else BoolVal(True)
        case ValueType.Null:
            return BoolVal(False)
        case _:
            return NotImplementedVal()

def int(value: RuntimeVal) -> IntVal | NotImplementedVal:
    match value:
        case ValueType.Int:
            return value
        case ValueType.Bool: 
            return IntVal(0)
        case ValueType.Float:
            return IntVal(float(value.value))
        case ValueType.Str:
            try:
                return IntVal(int(value.value))
            except ValueError: 
                raise Exception()
        case ValueType.Null:
            return IntVal(0)
        case _:
            return NotImplementedVal()

def float(value: RuntimeVal) -> IntVal | NotImplementedVal:
    match value:
        case ValueType.Float:
            return value
        case ValueType.Int:
            return FloatVal(value)
        case ValueType.Bool: 
            return FloatVal(.0)
        case ValueType.Str:
            try:
                return FloatVal(float(value.value))
            except ValueError:
                raise Exception()
        case ValueType.Null:
            return IntVal(0)
        case _:
            return NotImplementedVal()