"""
This file consists of functions that process unary and binary operations, mainly using raw runtime values.
"""
import runtime.values as Value
from runtime.eval.conversions import bool
from runtime.values import RuntimeVal, Number

def eval_add(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the addition operator (`+`).
    """
    # num + num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        result = lhs.value + rhs.value
        if isinstance(result, float): 
            return Value.Float(result)
        return Value.Int(result)


def eval_sub(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the subtraction operator (`-`).
    """
    # num - num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        result = lhs.value - rhs.value
        if isinstance(result, float): 
            return Value.Float(result)
        return Value.Int(result)

def eval_mul(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the multiplication operator (`*`).
    """
    # num * num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        result = lhs.value * rhs.value
        if isinstance(result, float): 
            return Value.Float(result)
        return Value.Int(result)

def eval_true_div(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the floating-point, otherwise known as the true division operator (`/`).
    """
    # num / num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        if rhs.value == 0:
            raise Exception()
        result = lhs.value / rhs.value
        return Value.Float(result)

def eval_floor_div(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the integer, or float division operator (`//`).
    """
    # num // num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        if rhs.value == 0:
            raise Exception()
        result = lhs.value // rhs.value
        return Value.Float(result)

def eval_mod(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the modulus operator (`%`).
    """
    # num % num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        if rhs.value == 0:
            raise Exception()
        result = lhs.value % rhs.value
        if isinstance(result, float): 
            return Value.Float(result)
        return Value.Int(result)

def eval_pow(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the exponentiation operator (`**`).
    """
    # num ** num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        result = lhs.value ** rhs.value
        if isinstance(result, float):
            return Value.Float(result)
        return Value.Int(result)

def eval_lt(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the less operator (`<`).
    """
    # num < num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        result = lhs.value < rhs.value
        
        if result:
            return Value.Bool(True)
        return Value.Bool(False)

def eval_gt(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the greater operator (`>`).
    """
    # num > num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        result = lhs.value > rhs.value
        
        if result:
            return Value.Bool(True)
        return Value.Bool(False)

def eval_le(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the less-or-equal operator (`<=`).
    """
    # num <= num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        result = lhs.value <= rhs.value
        
        if result:
            return Value.Bool(True)
        return Value.Bool(False)

def eval_ge(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the greater-or-equal operator (`>=`).
    """
    # num >= num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        result = lhs.value >= rhs.value
        
        if result:
            return Value.Bool(True)
        return Value.Bool(False)

def eval_eq(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the equality operator (`==`).
    """
    # num == num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        result = lhs.value == rhs.value
        
        if result:
            return Value.Bool(True)
        return Value.Bool(False)

def eval_ne(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the inequality operator (`!=`).
    """
    # num != num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        result = lhs.value != rhs.value
        
        if result:
            return Value.Bool(True)
        return Value.Bool(False)

def eval_spaceship(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the spaceship operator (`<=>`).
    """
    # num <=> num
    if isinstance(lhs, Number) and isinstance(rhs, Number):
        if lhs.value < rhs.value:
            return Value.Int(-1)
        if lhs.value == rhs.value:
            return Value.Int(0)
        return Value.Int(1)

def eval_concat(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the string concatenation operator (`..`).
    """
    # str .. str
    if isinstance(lhs, Value.Str) and isinstance(rhs, Value.Str):
        return Value.Str(lhs.value + rhs.value)

def eval_matmul(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the matrix multiplication operator (`@`).
    """

def eval_coalescing(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the null coalescing operator (`??`).
    """
    if isinstance(lhs, Value.Null):
        return rhs
    return lhs

def eval_elvis(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Processes operations using the Elvis operator (`?:`).
    """
    if bool(lhs).value:
        return lhs
    return rhs