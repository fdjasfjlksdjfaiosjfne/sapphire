from __future__ import annotations

from runtime.values.value_types import *
from runtime.values.value_attributes import *

INT_TYPE = Type("int", methods = NUMBER_METHODS)
FLOAT_TYPE = Type("float", methods = NUMBER_METHODS)
BOOL_TYPE = Type("bool", bases = [INT_TYPE], methods = BOOL_METHODS)
NULL_TYPE = Type("null", methods = {})
FUNCTION_TYPE = Type("function", methods = {})

RuntimeValue.attributes = RUNTIME_VAL_METHODS
IntValue.type = INT_TYPE
FloatValue.type = FLOAT_TYPE
BoolValue.type = BOOL_TYPE
NullValue.type = NULL_TYPE
FunctionValue.type = FUNCTION_TYPE