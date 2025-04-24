import parser.nodes as Nodes
import runtime.values as Value
from runtime.values import RuntimeVal, Number
from lexer.tokens import TokenType

def bool(value: RuntimeVal) -> Value.Bool | Value.NotImplemented:
    if isinstance(value, Value.Bool):
        return value
    elif isinstance(value, Number):
        return Value.Bool(False) if value.value == 0 else Value.Bool(True)
    elif isinstance(value, Value.Str):
        return Value.Bool(False) if value.value == "" else Value.Bool(True)
    elif isinstance(value, Value.Null):
        return Value.Bool(False)
    else:
        return Value.NotImplemented()

def int(value: RuntimeVal) -> Value.Int | Value.NotImplemented:
    if isinstance(value, Value.Int):
        return value
    elif isinstance(value, Value.Bool):
        return Value.Int(1) if value.value else Value.Int(0)
    elif isinstance(value, Value.Float):
        return Value.Int(int(value.value))
    elif isinstance(value, Value.Str):
        try:
            return Value.Int(int(value.value))
        except ValueError: 
            raise Exception()
    elif isinstance(value, Value.Null):
        return Value.Int(0)
    else:
        return Value.NotImplemented()

def float(value: RuntimeVal) -> Value.Int | Value.NotImplemented:
    if isinstance(value, Value.Float):
        return value
    elif isinstance(value, Value.Int):
        return Value.Float(float(value))
    elif isinstance(value, Value.Bool): 
        return Value.Float(1.) if value.value else Value.Float(0.)
    elif isinstance(value, Value.Str):
        try:
            return Value.Float(float(value.value))
        except ValueError:
            raise Exception()
    elif isinstance(value, Value.Null):
        return Value.Float(0)
    else:
        return Value.NotImplemented()