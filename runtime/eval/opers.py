"""
This modules consists of functions that process unary and binary operations, mainly using raw runtime values.
"""
import typing

import runtime.values as values
from runtime.values import RuntimeVal, Number

# Github Copilot write this
def _eval_binary_operation(
    lhs: RuntimeVal, 
    rhs: RuntimeVal,
    left_method: str,
    right_method: str,
    normal_method: str | None,
    type_check: typing.Callable[[RuntimeVal], bool] | None = None
) -> RuntimeVal:
    """
    Generic handler for binary operations that follow the pattern:
    - Try left special method
    - Try right special method 
    - Try normal method on left
    - Try normal method on right
    
    Args:
        lhs: Left-hand operand
        rhs: Right-hand operand
        left_method: Name of left special method (e.g. "__ladd__")
        right_method: Name of right special method (e.g. "__radd__")
        normal_method: Name of normal method (e.g. "__add__"). If omitted, skip the process.
        type_check: Optional function to validate return type
    """
    # Try left special method
    lhs_left: typing.Callable[[RuntimeVal], RuntimeVal] | None = lhs.__sap_props__.get(left_method)
    if callable(lhs_left):
        val = lhs_left(lhs, rhs)
        if not isinstance(val, values.NOT_IMPLEMENTED):
            if type_check and not type_check(val):
                raise Exception(f"Invalid return type from {left_method}")
            return val

    # Try right special method    
    rhs_right: typing.Callable[[RuntimeVal], RuntimeVal] | None = rhs.__sap_props__.get(right_method)
    if callable(rhs_right):
        val = rhs_right(rhs, lhs)
        if not isinstance(val, values.NOT_IMPLEMENTED):
            if type_check and not type_check(val):
                raise Exception(f"Invalid return type from {right_method}")
            return val

    if normal_method is not None:
        # Try normal method on left
        lhs_normal: typing.Callable[[RuntimeVal, bool], RuntimeVal] | None = lhs.__sap_props__.get(normal_method)
        if callable(lhs_normal):
            val = lhs_normal(lhs, rhs, False)
            if not isinstance(val, values.NOT_IMPLEMENTED):
                if type_check and not type_check(val):
                    raise Exception(f"Invalid return type from {normal_method}")
                return val

        # Try normal method on right
        rhs_normal: typing.Callable[[RuntimeVal, bool], RuntimeVal] | None = rhs.__sap_props__.get(normal_method)
        if callable(rhs_normal):
            val = rhs_normal(rhs, lhs, True)
            if not isinstance(val, values.NOT_IMPLEMENTED):
                if type_check and not type_check(val):
                    raise Exception(f"Invalid return type from {normal_method}")
                return val

    raise Exception("Operation not supported between these types")

def eval_add(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the addition operator ('+')."""
    return _eval_binary_operation(lhs, rhs, "__ladd__", "__radd__", "__add__")

def eval_sub(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the subtraction operator ('-').""" 
    return _eval_binary_operation(lhs, rhs, "__lsub__", "__rsub__", "__sub__")

def eval_mul(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the multiplication operator ('*')."""
    return _eval_binary_operation(lhs, rhs, "__lmul__", "__rmul__", "__mul__")

def eval_truediv(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the floating-point division operator ('/')."""
    return _eval_binary_operation(lhs, rhs, "__ltruediv__", "__rtruediv__", "__truediv__")

def eval_floordiv(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the floor division operator ('//')."""
    return _eval_binary_operation(lhs, rhs, "__lfloordiv__", "__rfloordiv__", "__floordiv__")

def eval_mod(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the modulus operator ('%')."""
    return _eval_binary_operation(lhs, rhs, "__lmod__", "__rmod__", "__mod__")

def eval_exp(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the exponentiation operator ('**')."""
    return _eval_binary_operation(lhs, rhs, "__lexp__", "__rexp__", "__exp__")

def eval_concat(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the string concatenation operator ('..')."""
    return _eval_binary_operation(lhs, rhs, "__lconcat__", "__rconcat__", "__concat__")

def eval_matmul(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the matrix multiplication operator ('@')."""
    return _eval_binary_operation(lhs, rhs, "__lmatmul__", "__rmatmul__", "__matmul__")

def eval_and(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the logical AND operator ('&&' / 'and')."""
    return _eval_binary_operation(lhs, rhs, "__land__", "__rand__", "__and__")

def eval_or(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the logical OR operator ('||' / 'or')."""
    return _eval_binary_operation(lhs, rhs, "__lor__", "__ror__", "__or__")

def eval_xor(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the logical XOR operator ('^^' / 'xor')."""
    return _eval_binary_operation(lhs, rhs, "__lxor__", "__rxor__", "__xor__")

def eval_sps(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """Process operations using the spaceship operator ('<=>').

    Must return a Number."""
    return _eval_binary_operation(
        lhs, rhs, 
        "__lsps__", "__rsps__", "__sps__",
        lambda x: isinstance(x, (values.Int, values.Float))
    )

def eval_lt(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Process operations using the less operator ('<').
    The checking process is as follows, from top to bottom:
    - Run lhs's __lt__(other)
    - Run rhs's __gt__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, "__lt__", "__gt__")
    except:
        return eval_sps(lhs, rhs) < 0

def eval_gt(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Process operations using the greater operator ('>').
    The checking process is as follows, from top to bottom:
    - Run lhs's __gt__(other)
    - Run rhs's __lt__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, "__gt__", "__lt__")
    except:
        return eval_sps(lhs, rhs) > 0

def eval_le(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Process operations using the less-or-equal operator ('<=').
    The checking process is as follows, from top to bottom:
    - Run lhs's __le__(other)
    - Run rhs's __ge__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, "__le__", "__ge__")
    except:
        return eval_sps(lhs, rhs) <= 0

def eval_ge(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Process operations using the greater-or-equal operator ('>=').
    The checking process is as follows, from top to bottom:
    - Run lhs's __le__(other)
    - Run rhs's __ge__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, "__ge__", "__le__")
    except:
        return eval_sps(lhs, rhs) >= 0

def eval_eq(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Process operations using the less operator ('==').
    The checking process is as follows, from top to bottom:
    - Run lhs's __lt__(other)
    - Run rhs's __gt__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, "__eq__", "__eq__")
    except:
        return eval_sps(lhs, rhs) == 0

def eval_ne(lhs: RuntimeVal, rhs: RuntimeVal) -> RuntimeVal:
    """
    Process operations using the less operator ('<').
    The checking process is as follows, from top to bottom:
    - Run lhs's __lt__(other)
    - Run rhs's __gt__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, "__ne__", "__ne__")
    except:
        return eval_sps(lhs, rhs) != 0

def eval_increment(expr: RuntimeVal) -> RuntimeVal:
    """
    Process operations using the increment operator ('++').
    The checking is as follows, from top to bottom:
    - Run expr.__incre__()
    - Run expr.__iadd__(1), which, by itself, will call __add__, __ladd__ and __radd__ as fallback
    """
    from runtime.eval.inplaceops import eval_iadd
    incre_fn: typing.Callable[[], RuntimeVal] | None = expr.__sap_props__.get("__incre__")
    if callable(incre_fn):
        val = incre_fn()
        if not isinstance(val, values.NOT_IMPLEMENTED):
            return val
    return eval_iadd(expr, values.Int(1))

def eval_decrement(expr: RuntimeVal) -> RuntimeVal:
    """
    Process operations using the decrement operator ('--').
    The checking is as follows, from top to bottom:
    - Run expr.__decre__()
    - Run expr.__isub__(1), which, by itself, will call __sub__, __lsub__ and __rsub__ as fallback
    """
    from runtime.eval.inplaceops import eval_isub
    decre_fn: typing.Callable[[], RuntimeVal] | None = expr.__sap_props__.get("__decre__")
    if callable(decre_fn):
        val = decre_fn()
        if not isinstance(val, values.NOT_IMPLEMENTED):
            return val
    return eval_isub(expr, values.Int(1))