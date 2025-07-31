from __future__ import annotations

from runtime._values.value_attributes import (
    RUNTIME_VAL_METHODS, NUMBER_METHODS, 
    INT_METHODS, STR_METHODS, BOOL_METHODS, 
    NULL_METHODS, LIST_METHODS, TUPLE_METHODS, 
    SET_METHODS, DICT_METHODS, FUNCTION_METHODS
)

from runtime._values.value_types import (
    TRUE, FALSE, NULL, NOT_IMPLEMENTED,
    RuntimeValue, Type, NumberValue,
    IntValue, FloatValue, BoolValue,
    StringValue, NullValue, FunctionValue,
    NativeFunctionValue, CustomFunctionValue,
    BoundCustomFunction, ListValue, TupleValue,
    SetValue, DictValue
)

OBJECT_TYPE = Type("object", methods = RUNTIME_VAL_METHODS)
NUMBER_TYPE = Type("number", methods = NUMBER_METHODS)
INT_TYPE = Type("int", bases = [NUMBER_TYPE], methods = INT_METHODS)
FLOAT_TYPE = Type("float", bases = [NUMBER_TYPE])
STR_TYPE = Type("str", methods = STR_METHODS)
BOOL_TYPE = Type("bool", bases = [INT_TYPE], methods = BOOL_METHODS)
NULL_TYPE = Type("null", methods = NULL_METHODS)
FUNCTION_TYPE = Type("function", methods = FUNCTION_METHODS)
LIST_TYPE = Type("list", methods = LIST_METHODS)
TUPLE_TYPE = Type("tuple", methods = TUPLE_METHODS)
SET_TYPE = Type("set", methods = SET_METHODS)
DICT_TYPE = Type("dict", methods = DICT_METHODS)

RuntimeValue.type = OBJECT_TYPE
NumberValue.type = NUMBER_TYPE
IntValue.type = INT_TYPE
FloatValue.type = FLOAT_TYPE
StringValue.type = STR_TYPE
BoolValue.type = BOOL_TYPE
NullValue.type = NULL_TYPE
FunctionValue.type = FUNCTION_TYPE
ListValue.type = LIST_TYPE
TupleValue.type = TUPLE_TYPE
SetValue.type = SET_TYPE
DictValue.type = DICT_TYPE