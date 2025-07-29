"""
This file consists of functions that process inplace, also known as augmented or modifier assignments, mainly using raw runtime values.
"""
import typing
import runtime._expriemental.values as values
import backend.errors as errors
from runtime.eval import opers


def _eval_inplace_operation(
        lhs: values.RuntimeVal,
        rhs: values.RuntimeVal,
        right: bool,
        inplace_name: str,
        fallback: typing.Callable[[values.RuntimeVal, values.RuntimeVal], values.RuntimeVal],
    ) -> None:
    """Generic handler for inplace operations.
    """
    
    inplace_method: typing.Callable[[values.RuntimeVal, values.RuntimeVal, values.Bool], values.RuntimeVal] = lhs.sap_props.get(inplace_name)
    if callable(inplace_method):
        val = inplace_method(lhs, rhs, values.Bool(right))
        if not isinstance(val, values.NOT_IMPLEMENTED):
            return val
    ...
    return fallback(lhs, rhs)



def eval_iadd(lhs: values.RuntimeVal, rhs: values.RuntimeVal, right: bool) -> None:
    """
    Processes operations using the addition in-place operator (`+=`).
    """
    return _eval_inplace_operation(lhs, rhs, right, "__iadd__", opers.eval_add)



def eval_isub(lhs: values.RuntimeVal, rhs: values.RuntimeVal, right: bool) -> None:
    """
    Processes operations using the subtraction in-place operator (`-=`).
    """
    return _eval_inplace_operation(lhs, rhs, right, "__isub__", opers.eval_sub)

def eval_imul(lhs: values.RuntimeVal, rhs: values.RuntimeVal, right: bool) -> None:
    """
    Processes operations using the multiplication in-place operator (`*=`).
    """
    return _eval_inplace_operation(lhs, rhs, right, "__imul__", opers.eval_mul)

def eval_itruediv(lhs: values.RuntimeVal, rhs: values.RuntimeVal, right: bool) -> None:
    """
    Processes operations using the floating-point, otherwise known as the true division in-place operator (`/=`).
    """
    return _eval_inplace_operation(lhs, rhs, right, "__itruediv__", opers.eval_truediv)

def eval_ifloordiv(lhs: values.RuntimeVal, rhs: values.RuntimeVal, right: bool) -> None:
    """
    Processes operations using the integer, or float division operator (`//=`).
    """
    return _eval_inplace_operation(lhs, rhs, right, "__ifloordiv__", opers.eval_floordiv)

def eval_imod(lhs: values.RuntimeVal, rhs: values.RuntimeVal, right: bool) -> None:
    """
    Processes operations using the modulus in-place operator (`%=`).
    """
    return _eval_inplace_operation(lhs, rhs, right, "__imod__", opers.eval_mod)

def eval_iexp(lhs: values.RuntimeVal, rhs: values.RuntimeVal, right: bool) -> None:
    """
    Processes operations using the exponentiation in-place operator (`**=`).
    """
    return _eval_inplace_operation(lhs, rhs, right, "__iexp__", opers.eval_exp)

def eval_iconcat(lhs: values.RuntimeVal, rhs: values.RuntimeVal, right: bool) -> None:
    """
    Processes operations using the string concatenation in-place operator (`..=`).
    """
    return _eval_inplace_operation(lhs, rhs, right, "__iconcat__", opers.eval_concat)

def eval_imatmul(lhs: values.RuntimeVal, rhs: values.RuntimeVal, right: bool) -> None:
    """
    Processes operations using the matrix multiplication in-place operator (`@=`).
    """
    return _eval_inplace_operation(lhs, rhs, right, "__imatmul__", opers.eval_matmul)