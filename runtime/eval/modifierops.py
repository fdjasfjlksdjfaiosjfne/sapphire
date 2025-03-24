"""
This file consists of functions that process unary and binary operations, mainly using raw runtime values.
"""
import runtime.values as Value
from runtime.values import ValueType, RuntimeVal
from runtime.env import Env

def eval_add(ident: str, rhs: RuntimeVal, env: Env) -> None:
    """
    Processes operations using the addition in-place operator (`+=`).
    """
    val = env.get(ident)
    # num + num
    if ValueType.Number @ [val, rhs]:
        result = val.value + rhs.value
        if isinstance(result, float): 
            env.assign(ident, result)
        env.assign(ident, result)


def eval_sub(ident: str, rhs: RuntimeVal, env: Env) -> None:
    """
    Processes operations using the subtraction in-place operator (`-=`).
    """
    val = env.get(ident)
    # num - num
    if ValueType.Number @ [val, rhs]:
        result = val.value - rhs.value
        if isinstance(result, float): 
            env.assign(ident, result)
        env.assign(ident, result)

def eval_mul(ident: str, rhs: RuntimeVal, env: Env) -> None:
    """
    Processes operations using the multiplication in-place operator (`*=`).
    """
    val = env.get(ident)
    # num * num
    if ValueType.Number @ [val, rhs]:
        result = val.value * rhs.value
        if isinstance(result, float): 
            env.assign(ident, result)
        env.assign(ident, result)

def eval_true_div(ident: str, rhs: RuntimeVal, env: Env) -> None:
    """
    Processes operations using the floating-point, otherwise known as the true division in-place operator (`/=`).
    """
    val = env.get(ident)
    # num / num
    if ValueType.Number @ [val, rhs]:
        result = val.value / rhs.value
        env.assign(ident, result)

def eval_floor_div(ident: str, rhs: RuntimeVal, env: Env) -> None:
    """
    Processes operations using the integer, or float division operator (`//=`).
    """
    val = env.get(ident)
    # num // num
    if ValueType.Number @ [val, rhs]:
        result = val.value // rhs.value
        env.assign(ident, result)

def eval_mod(ident: str, rhs: RuntimeVal, env: Env) -> None:
    """
    Processes operations using the modulus in-place operator (`%=`).
    """
    val = env.get(ident)
    # num % num
    if ValueType.Number @ [val, rhs]:
        result = val.value % rhs.value
        if isinstance(result, float): 
            env.assign(ident, result)
        env.assign(ident, result)

def eval_pow(ident: str, rhs: RuntimeVal, env: Env) -> None:
    """
    Processes operations using the exponentiation in-place operator (`**=`).
    """
    val = env.get(ident)
    # num ** num
    if ValueType.Number @ [val, rhs]:
        result = val.value ** rhs.value
        if isinstance(result, float):
            env.assign(ident, result)
        env.assign(ident, result)

def eval_concat(ident: str, rhs: RuntimeVal, env: Env) -> None:
    """
    Processes operations using the string concatenation in-place operator (`..=`).
    """
    val = env.get(ident)
    # str .. str
    if ValueType.Str @ [val, rhs]:
        return Value.Str(val.value + rhs.value)

def eval_matmul(ident: str, rhs: RuntimeVal, env: Env) -> None:
    """
    Processes operations using the matrix multiplication in-place operator (`@=`).
    """

def eval_coalescing(ident: str, rhs: RuntimeVal, env: Env) -> None:
    """
    Processes operations using the null coalescing in-place operator (`??=`).
    """
    val = env.get(ident)
    if val == ValueType.Null:
        env.assign(ident, rhs.value)