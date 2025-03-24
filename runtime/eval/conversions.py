import parser.nodes as Node
import runtime.values as Value
from runtime.values import ValueType
from lexer.tokens import TokenType

def bool(value: Value.RuntimeVal) -> Value.Bool | Value.NotImplementedVal:
    match value:
        case ValueType.Bool: 
            return value
        case ValueType.Int | ValueType.Float:
            return Value.Bool(False) if value == 0 else Value.Bool(True)
        case ValueType.Str:
            return Value.Bool(False) if value == "" else Value.Bool(True)
        case ValueType.Null:
            return Value.Bool(False)
        case _:
            return Value.NotImplementedVal()

def int(value: Value.RuntimeVal) -> Value.Int | Value.NotImplementedVal:
    match value:
        case ValueType.Int:
            return value
        case ValueType.Bool: 
            return Value.Int(1) if value.value else Value.Int(0)
        case ValueType.Float:
            return Value.Int(int(value.value))
        case ValueType.Str:
            try:
                return Value.Int(int(value.value))
            except ValueError: 
                raise Exception()
        case ValueType.Null:
            return Value.Int(0)
        case _:
            return Value.NotImplementedVal()

def float(value: Value.RuntimeVal) -> Value.Int | Value.NotImplementedVal:
    match value:
        case ValueType.Float:
            return value
        case ValueType.Int:
            return Value.Float(float(value))
        case ValueType.Bool: 
            return Value.Float(1.) if value.value else Value.Float(0.)
        case ValueType.Str:
            try:
                return Value.Float(float(value.value))
            except ValueError:
                raise Exception()
        case ValueType.Null:
            return Value.Float(0)
        case _:
            return Value.NotImplementedVal()