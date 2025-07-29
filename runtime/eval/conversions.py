
# @ This module is deprecated
# @ Please use __init__ from value wrappers runtime.values modules instead

import warnings
import parser.nodes as Nodes
import runtime._expriemental.values as values
from runtime._expriemental.values import RuntimeVal, Number

raise DeprecationWarning("Please use '__init__()' from value wrappers from 'runtime.values' instead.")

def bool(value: RuntimeVal) -> values.Bool | values.NOT_IMPLEMENTED:
    if isinstance(value, values.Bool):
        return value
    elif isinstance(value, Number):
        return values.Bool(False) if value.value == 0 else values.Bool(True)
    elif isinstance(value, values.Str):
        return values.Bool(False) if value.value == "" else values.Bool(True)
    elif isinstance(value, values.Null):
        return values.Bool(False)
    else:
        return values.NOT_IMPLEMENTED()

def int(value: RuntimeVal) -> values.Int | values.NOT_IMPLEMENTED:
    if isinstance(value, values.Int):
        return value
    elif isinstance(value, values.Bool):
        return values.Int(1) if value.value else values.Int(0)
    elif isinstance(value, values.Float):
        return values.Int(int(value.value))
    elif isinstance(value, values.Str):
        try:
            return values.Int(int(value.value))
        except ValueError: 
            raise Exception()
    elif isinstance(value, values.Null):
        return values.Int(0)
    else:
        return values.NOT_IMPLEMENTED()

def float(value: RuntimeVal) -> values.Int | values.NOT_IMPLEMENTED:
    if isinstance(value, values.Float):
        return value
    elif isinstance(value, values.Int):
        return values.Float(float(value))
    elif isinstance(value, values.Bool): 
        return values.Float(1.) if value.value else values.Float(0.)
    elif isinstance(value, values.Str):
        try:
            return values.Float(float(value.value))
        except ValueError:
            raise Exception()
    elif isinstance(value, values.Null):
        return values.Float(0)
    else:
        return values.NOT_IMPLEMENTED()