"""
This file consists of functions that process inplace, also known as augmented or modifier assignments, mainly using raw runtime values.
"""
import typing
import runtime.values as values
import backend.errors as errors
from runtime.eval import binops


def _eval_inplace_operation(
        lhs: values.RuntimeVal, 
        rhs: values.RuntimeVal, 
        inplace_name: str,
        fallback: typing.Callable[[values.RuntimeVal, values.RuntimeVal], values.RuntimeVal],
    ) -> None:
    """Generic handler for inplace operations.
    """
    
    inplace_method: typing.Callable[[values.RuntimeVal, values.RuntimeVal], values.RuntimeVal] = lhs.sap_props.get(inplace_name)
    if callable(inplace_method):
        val = inplace_method(lhs, rhs)
        if not isinstance(val, values.NOT_IMPLEMENTED):
            return val
    
    return fallback(lhs, rhs)



def eval_iadd(lhs: values.RuntimeVal, rhs: values.RuntimeVal) -> None:
    """
    Processes operations using the addition in-place operator (`+=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__iadd__", binops.eval_add)



def eval_isub(lhs: values.RuntimeVal, rhs: values.RuntimeVal) -> None:
    """
    Processes operations using the subtraction in-place operator (`-=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__isub__", binops.eval_sub)

def eval_imul(lhs: values.RuntimeVal, rhs: values.RuntimeVal) -> None:
    """
    Processes operations using the multiplication in-place operator (`*=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__imul__", binops.eval_mul)

def eval_itruediv(lhs: values.RuntimeVal, rhs: values.RuntimeVal) -> None:
    """
    Processes operations using the floating-point, otherwise known as the true division in-place operator (`/=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__itruediv__", binops.eval_truediv)

def eval_ifloordiv(lhs: values.RuntimeVal, rhs: values.RuntimeVal) -> None:
    """
    Processes operations using the integer, or float division operator (`//=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__ifloordiv__", binops.eval_floordiv)

def eval_imod(lhs: values.RuntimeVal, rhs: values.RuntimeVal) -> None:
    """
    Processes operations using the modulus in-place operator (`%=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__imod__", binops.eval_mod)

def eval_iexp(lhs: values.RuntimeVal, rhs: values.RuntimeVal) -> None:
    """
    Processes operations using the exponentiation in-place operator (`**=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__iexp__", binops.eval_exp)

def eval_iconcat(lhs: values.RuntimeVal, rhs: values.RuntimeVal) -> None:
    """
    Processes operations using the string concatenation in-place operator (`..=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__iconcat__", binops.eval_concat)

def eval_imatmul(lhs: values.RuntimeVal, rhs: values.RuntimeVal) -> None:
    """
    Processes operations using the matrix multiplication in-place operator (`@=`).
    """
    return _eval_inplace_operation(lhs, rhs, "__imatmul__", binops.eval_matmul)