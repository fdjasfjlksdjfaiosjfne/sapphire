from __future__ import annotations

import ast
import functools
import inspect
import itertools
import operator
import typing

from backend import errors
from runtime._values.value_types import (
    RuntimeValue,
    Type,
    NumberValue,
    IntValue,
    FloatValue,
    BoolValue,
    StringValue,
    NullValue,
    FunctionValue,
    NativeFunctionValue,
    CustomFunctionValue,
    BoundCustomFunction,
    ListValue,
    TupleValue,
    SetValue,
    DictValue,
    TRUE,
    FALSE,
    NOT_IMPLEMENTED,
    NULL
)
from backend.config import CONFIG

_name_counter = itertools.count()
def _generate_unique_name(exclusions: typing.Sequence[str] | None = None) -> str:
    if exclusions is None:
        exclusions = tuple()
    for _ in range(1000):
        name = f"_func_{next(_name_counter)}"
        if name not in exclusions:
            return name
    raise errors.InternalError()

def _turn_into_dict(fn) -> dict[str, typing.Any]:
    @functools.wraps(fn)
    def decorator() -> dict[str, typing.Any]:
        source = inspect.getsource(inspect.unwrap(fn))
        ast_tree = ast.parse(source)

        
        if (not ast_tree.body[0] 
            or not isinstance(ast_tree.body[0], (ast.FunctionDef, ast.ClassDef))):
            raise errors.InternalError(
                "@_turn_into_dict() must be attached into a class or function declaration"
            )
        namespace: dict[str, typing.Any] = {}
        result = {}
        fn_or_cls_tree = ast_tree.body[0]

        for node in fn_or_cls_tree.body:
            if isinstance(node, ast.FunctionDef):
                original_name = node.name[:]
                node.name = _generate_unique_name(list(namespace.keys()))

                # from __future__ import annotations
                annotations_directive = ast.ImportFrom(
                    module = "__future__",
                    names = [ast.alias(
                                name = "annotations",
                                asname = None
                            )],
                    level = 0
                )
                exec(compile(ast.fix_missing_locations(ast.Module(body=[node],
                                                                  type_ignores=[])), 
                             "<ast>", "exec"
                            ),
                     namespace
                    )
                
                func = namespace[node.name]
                func.__name__ = original_name
                result[original_name] = func
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        result[target.id] = node.value
        return result
    return decorator()

@_turn_into_dict
def RUNTIME_VAL_METHODS():
    def __getattribute__(self, attr):
        assert isinstance(self, RuntimeValue)
        return self.get_attribute(attr)

    def __bool__(self):
        return TRUE

    def __logicand__(self, other, right):
        assert isinstance(self, RuntimeValue) and isinstance(other, RuntimeValue)
        lhs, rhs = (other, self) if right else (self, other)
        if not BoolValue(lhs).value:
            if CONFIG.customization.logical_operator_behavior == "boolean_only":
                return FALSE
            return lhs
        if CONFIG.customization.logical_operator_behavior == "boolean_only":
            return BoolValue(rhs)
        return rhs
    
    def __logicor__(self, other, right):
        assert isinstance(self, RuntimeValue) and isinstance(other, RuntimeValue)
        lhs, rhs = (other, self) if right else (self, other)
        if BoolValue(lhs).value:
            if CONFIG.customization.logical_operator_behavior == "boolean_only":
                return TRUE
            return lhs
        if CONFIG.customization.logical_operator_behavior == "boolean_only":
            return BoolValue(rhs)
        return rhs
    
    def __logicxor__(self, other, right):
        assert isinstance(self, RuntimeValue) and isinstance(other, RuntimeValue)
        if BoolValue(self).value == BoolValue(other).value:
            return FALSE
        
        if CONFIG.customization.logical_operator_behavior != "extended_pythonic":
            return TRUE
        
        if BoolValue(self).value:
            return self
        return other

@_turn_into_dict
def NUMBER_METHODS():
    def __int__(self):
        assert isinstance(self, (IntValue, FloatValue))
        return IntValue(self.value)

    def __float__(self):
        assert isinstance(self, (IntValue, FloatValue))
        return FloatValue(self.value)

    def __add__(self, other, right):
        return _commutative_numeric_operation(operator.add)(self, other)

    def __sub__(self, other, right):
        return _non_commutative_numeric_operation(operator.sub)(self, other, right)
    
    def __mul__(self, other, right):
        return _commutative_numeric_operation(operator.mul)(self, other)

    def __truediv__(self, other, right):
        return _non_commutative_numeric_operation(operator.truediv)(self, other, right)
    
    def __floordiv__(self, other, right):
        return _non_commutative_numeric_operation(operator.floordiv)(self, other, right)
    
    def __mod__(self, other, right):
        return _non_commutative_numeric_operation(operator.mod)(self, other, right)
    
    def __exp__(self, other, right):
        return _non_commutative_numeric_operation(operator.pow)(self, other, right)
    
    def __le__(self, other):
        return _comparison_numeric_operation(operator.le)(self, other)
    
    def __ge__(self, other):
        return _comparison_numeric_operation(operator.ge)(self, other)
    
    def __lt__(self, other):
        return _comparison_numeric_operation(operator.lt)(self, other)
    
    def __gt__(self, other):
        return _comparison_numeric_operation(operator.gt)(self, other)
    
    def __eq__(self, other):
        return _comparison_numeric_operation(operator.eq)(self, other)
    
    def __ne__(self, other):
        return _comparison_numeric_operation(operator.ne)(self, other)

@_turn_into_dict
def INT_METHODS():
    def __binand__(self, other, right):
        return _commutative_numeric_operation(operator.and_)(self, other)
    def __binor__(self, other, right):
        return _commutative_numeric_operation(operator.or_)(self, other)
    def __binxor__(self, other, right):
        return _commutative_numeric_operation(operator.xor)(self, other)

@_turn_into_dict
def STR_METHODS():
    def __int__(self):
        assert isinstance(self, StringValue)
        return IntValue(int(self.value))

    def __float__(self):
        assert isinstance(self, StringValue)
        return FloatValue(float(self.value))

    def __str__(self):
        assert isinstance(self, StringValue)
        return self
    
    def capitalize(self):
        assert isinstance(self, StringValue)
        return StringValue(self.value.capitalize())
    
    def casefold(self):
        assert isinstance(self, StringValue)
        return StringValue(self.value.casefold())
    
    def lower(self):
        assert isinstance(self, StringValue)
        return StringValue(self.value.lower())
    
    def isalnum(self):
        assert isinstance(self, StringValue)
        return BoolValue(self.value.isalnum())
    
    def isalpha(self):
        assert isinstance(self, StringValue)
        return BoolValue(self.value.isalpha())
    
    def isdigit(self):
        assert isinstance(self, StringValue)
        return BoolValue(self.value.isdigit())
    
    def isidentifier(self):
        assert isinstance(self, StringValue)
        return self.value.isidentifier()
    
    def upper(self):
        assert isinstance(self, StringValue)
        return StringValue(self.value.upper())

    def title(self):
        assert isinstance(self, StringValue)
        return StringValue(self.value.title())
    
    def swapcase(self):
        assert isinstance(self, StringValue)
        return StringValue(self.value.swapcase())
    
    def strip(self, chars):
        assert (isinstance(self, StringValue) 
                and (isinstance(chars, StringValue) 
                     or chars is NULL))

        if isinstance(chars, StringValue):
            ch = chars.value
        else:
            assert chars is NULL
            ch = None
        
        return StringValue(self.value.strip(ch))
    
    def lstrip(self, chars):
        assert (isinstance(self, StringValue) 
                and (isinstance(chars, StringValue) 
                     or chars is NULL))
        
        if isinstance(chars, StringValue):
            ch = chars.value
        else:
            assert chars is NULL
            ch = None
        
        return StringValue(self.value.lstrip(ch))

    def rstrip(self, chars):
        assert (isinstance(self, StringValue) 
                and (isinstance(chars, StringValue) 
                     or chars is NULL))
        
        if isinstance(chars, StringValue):
            ch = chars.value
        else:
            assert chars is NULL
            ch = None
        
        return StringValue(self.value.rstrip(ch))

    def __concat__(self, other, right):
        assert isinstance(self, StringValue)
        if not isinstance(other, StringValue):
            return NOT_IMPLEMENTED
        lhs, rhs = (other, self) if right else (self, other)
        return StringValue(lhs.value + rhs.value)
    
    def __lmul__(self, other):
        assert isinstance(self, StringValue)
        if not isinstance(other, IntValue):
            return NOT_IMPLEMENTED
        return StringValue(self.value * other.value)

    def __contains__(self, key):
        assert isinstance(self, StringValue)
        if not isinstance(key, StringValue):
            return NOT_IMPLEMENTED
        return BoolValue(key.value in self.value)

@_turn_into_dict
def BOOL_METHODS():
    def __bool__(self):
        assert isinstance(self, BoolValue)
        return self
    
    def __binand__(self, other, right):
        return _bool_and(self, other, right)
    def __binor__(self, other, right):
        return _bool_or(self, other, right)
    def __binxor__(self, other, right):
        return _bool_xor(self, other)
    
    def __and__(self, other, right):
        return _bool_and(self, other, right)
    def __or__(self, other, right):
        return _bool_or(self, other, right)
    def __xor__(self, other, right):
        return _bool_xor(self, other)

    def __logicand__(self, other, right):
        return _bool_and(self, other, right)
    def __logicor__(self, other, right):
        return _bool_or(self, other, right)
    def __logicxor__(self, other, right):
        return _bool_xor(self, other)

@_turn_into_dict
def FUNCTION_METHODS():
    pass

@_turn_into_dict
def NULL_METHODS():
    def __bool__(self):
        assert isinstance(self, NullValue)
        return True

@_turn_into_dict
def LIST_METHODS():
    def __list__(self):
        assert isinstance(self, ListValue)
        return self

@_turn_into_dict
def TUPLE_METHODS():
    def __tuple__(self):
        assert isinstance(self, TupleValue)
        return self

@_turn_into_dict
def SET_METHODS():
    def __set__(self):
        assert isinstance(self, SetValue)
        return self

@_turn_into_dict
def DICT_METHODS():
    def __dict__(self):
        assert isinstance(self, DictValue)
        return self

def _ignore(fn):
    return fn

def _commutative_numeric_operation(operation):
    def method(self, other):
        assert isinstance(self, (IntValue, FloatValue))
        if not isinstance(other, (IntValue, FloatValue)):
            return NOT_IMPLEMENTED
        if any(isinstance(i, FloatValue) for i in (self, other)):
            return FloatValue(operation(self.value, other.value))
        return IntValue(operation(self.value + other.value))
    return method

def _non_commutative_numeric_operation(operation: typing.Callable[[int|float, int|float], int|float]):
    """Create an non-commutative arithmetic method with the given operation"""
    def method(self, other, right=False):
        assert isinstance(self, (IntValue, FloatValue))
        if not isinstance(other, (IntValue, FloatValue)):
            return NOT_IMPLEMENTED
        
        will_be_float_val = any(isinstance(i, FloatValue) for i in (self, other))
        
        match (right, will_be_float_val):
            case (False, True):
                return FloatValue(operation(self.value, other.value))
            case (True, True):
                return FloatValue(operation(other.value, self.value))
            case (False, False):
                return IntValue(operation(self.value, other.value))
            case (True, False):
                return IntValue(operation(other.value, self.value))
        
        return NOT_IMPLEMENTED
    return method

def _comparison_numeric_operation(operation: typing.Callable[[int|float, int|float], bool]):
    def method(self, other):
        assert isinstance(self, (IntValue, FloatValue))
        if not isinstance(other, (IntValue, FloatValue)):
            return NOT_IMPLEMENTED
        return BoolValue(operation(self.value, other.value))
    return method

def _bool_and(self, other, right):
    assert isinstance(self, BoolValue) and isinstance(other, BoolValue)
    lhs, rhs = (other, self) if right else (self, other)
    if not lhs.value:
        return lhs
    return rhs

def _bool_or(self, other, right):
    assert isinstance(self, BoolValue) and isinstance(other, BoolValue)
    lhs, rhs = (other, self) if right else (self, other)
    if lhs.value:
        return lhs
    return rhs

def _bool_xor(self, other):
    assert isinstance(self, BoolValue) and isinstance(other, BoolValue)
    if self.value != other.value:
        return TRUE
    return FALSE