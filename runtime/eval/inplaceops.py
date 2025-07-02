"""
This file consists of functions that process inplace, also known as augmented or modifier assignments, mainly using raw runtime values.
"""
import typing
import runtime.values as Value
import backend.errors as errors
from runtime.eval import binops


def _eval_inplace_operation(
        lhs: Value.RuntimeVal, 
        rhs: Value.RuntimeVal, 
        inplace_name: str,
        fallback: typing.Callable[[Value.RuntimeVal, Value.RuntimeVal], Value.RuntimeVal],
    ) -> None:
    """Generic handler for inplace operations.
    """
    
    inplace_method: typing.Callable[[Value.RuntimeVal, Value.RuntimeVal], Value.RuntimeVal] = lhs.sap_props.get(inplace_name)
    if callable(inplace_method):
        val = inplace_method(lhs, rhs)
        if not isinstance(val, Value.NOT_IMPLEMENTED):
            return val
    
    return fallback(lhs, rhs)



def eval_add(lhs: Value.RuntimeVal, rhs: Value.RuntimeVal) -> None:
    """
    Processes operations using the addition in-place operator (`+=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__iadd__", binops.eval_add)



def eval_sub(lhs: Value.RuntimeVal, rhs: Value.RuntimeVal) -> None:
    """
    Processes operations using the subtraction in-place operator (`-=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__isub__", binops.eval_sub)

def eval_mul(lhs: Value.RuntimeVal, rhs: Value.RuntimeVal) -> None:
    """
    Processes operations using the multiplication in-place operator (`*=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__imul__", binops.eval_mul)

def eval_true_div(lhs: Value.RuntimeVal, rhs: Value.RuntimeVal) -> None:
    """
    Processes operations using the floating-point, otherwise known as the true division in-place operator (`/=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__itruediv__", binops.eval_truediv)

def eval_floor_div(lhs: Value.RuntimeVal, rhs: Value.RuntimeVal) -> None:
    """
    Processes operations using the integer, or float division operator (`//=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__ifloordiv__", binops.eval_floordiv)

def eval_mod(lhs: Value.RuntimeVal, rhs: Value.RuntimeVal) -> None:
    """
    Processes operations using the modulus in-place operator (`%=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__imod__", binops.eval_mod)

def eval_exp(lhs: Value.RuntimeVal, rhs: Value.RuntimeVal) -> None:
    """
    Processes operations using the exponentiation in-place operator (`**=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__iexp__", binops.eval_exp)

def eval_concat(lhs: Value.RuntimeVal, rhs: Value.RuntimeVal) -> None:
    """
    Processes operations using the string concatenation in-place operator (`..=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__iconcat__", binops.eval_concat)

def eval_matmul(lhs: Value.RuntimeVal, rhs: Value.RuntimeVal) -> None:
    """
    Processes operations using the matrix multiplication in-place operator (`@=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__imatmul__", binops.eval_matmul)

def eval_coalescing(ident: str, rhs: Value.RuntimeVal) -> None:
    """
    Processes operations using the null coalescing in-place operator (`??=`).
    """
    raise errors.InternalError("Not supported yet.")