import parser.nodes as N
import runtime.values as V
from runtime.values import ValueType
from lexer.tokens import TokenType

def bool(value: V.RuntimeVal) -> V.BoolVal | V.NotImplementedVal:
    match value:
        case ValueType.Bool: 
            return value
        case ValueType.Int | ValueType.Float:
            return V.BoolVal(False) if value == 0 else V.BoolVal(True)
        case ValueType.Str:
            return V.BoolVal(False) if value == "" else V.BoolVal(True)
        case ValueType.Null:
            return V.BoolVal(False)
        case _:
            return V.NotImplementedVal()

def int(value: V.RuntimeVal) -> V.IntVal | V.NotImplementedVal:
    match value:
        case ValueType.Int:
            return value
        case ValueType.Bool: 
            return V.IntVal(1) if value.value else V.IntVal(0)
        case ValueType.Float:
            return V.IntVal(int(value.value))
        case ValueType.Str:
            try:
                return V.IntVal(int(value.value))
            except ValueError: 
                raise Exception()
        case ValueType.Null:
            return V.IntVal(0)
        case _:
            return V.NotImplementedVal()

def float(value: V.RuntimeVal) -> V.IntVal | V.NotImplementedVal:
    match value:
        case ValueType.Float:
            return value
        case ValueType.Int:
            return V.FloatVal(float(value))
        case ValueType.Bool: 
            return V.FloatVal(1.) if value.value else V.FloatVal(0.)
        case ValueType.Str:
            try:
                return V.FloatVal(float(value.value))
            except ValueError:
                raise Exception()
        case ValueType.Null:
            return V.FloatVal(0)
        case _:
            return V.NotImplementedVal()