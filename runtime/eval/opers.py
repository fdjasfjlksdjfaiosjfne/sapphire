"""
This modules consists of functions that process unary and binary operations, mainly using raw runtime values.
"""
import typing

from runtime import env, values

# Github Copilot write this
def _eval_binary_operation(
    lhs: values.RuntimeValue, 
    rhs: values.RuntimeValue,
    env: env.Env,
    left_method: str,
    right_method: str,
    normal_method: str | None = None,
    type_check: typing.Callable[[values.RuntimeValue], bool] | None = None
) -> values.RuntimeValue:
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
    lhs_left = typing.cast(
        values.FunctionValue,
        lhs.get_attribute(left_method)
    )
    if callable(lhs_left):
        val = lhs_left.call(env, [rhs], {})
        if val is not values.NOT_IMPLEMENTED:
            if type_check and not type_check(val):
                raise Exception(f"Invalid return type from {left_method}")
            return val

    # Try right special method
    rhs_right = typing.cast(
        values.FunctionValue,
        rhs.get_attribute(right_method)
    )
    if callable(rhs_right):
        val = rhs_right.call(env, [lhs], {})
        if val is not values.NOT_IMPLEMENTED:
            if type_check and not type_check(val):
                raise Exception(f"Invalid return type from {right_method}")
            return val

    if normal_method is not None:
        # Try normal method on left
        lhs_normal = typing.cast(
            values.FunctionValue,
            lhs.get_attribute(normal_method)
        )
        if callable(lhs_normal):
            val = lhs_normal.call(env, [rhs, values.FALSE], {})
            if val is not values.NOT_IMPLEMENTED:
                if type_check and not type_check(val):
                    raise Exception(f"Invalid return type from {normal_method}")
                return val

        # Try normal method on right
        rhs_normal = typing.cast(values.FunctionValue, rhs.get_attribute(normal_method))
        if callable(rhs_normal):
            val = rhs_normal.call(env, [rhs, lhs, values.TRUE], {})
            if val is not values.NOT_IMPLEMENTED:
                if type_check and not type_check(val):
                    raise Exception(f"Invalid return type from {normal_method}")
                return val

    raise Exception("Operation not supported between these types")

def eval_add(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the addition operator ('+')."""
    return _eval_binary_operation(lhs, rhs, env, "__ladd__", "__radd__", "__add__")

def eval_sub(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the subtraction operator ('-').""" 
    return _eval_binary_operation(lhs, rhs, env, "__lsub__", "__rsub__", "__sub__")

def eval_mul(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the multiplication operator ('*')."""
    return _eval_binary_operation(lhs, rhs, env, "__lmul__", "__rmul__", "__mul__")

def eval_truediv(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the floating-point division operator ('/')."""
    return _eval_binary_operation(lhs, rhs, env, "__ltruediv__", "__rtruediv__", "__truediv__")

def eval_floordiv(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the floor division operator ('//')."""
    return _eval_binary_operation(lhs, rhs, env, "__lfloordiv__", "__rfloordiv__", "__floordiv__")

def eval_mod(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the modulus operator ('%')."""
    return _eval_binary_operation(lhs, rhs, env, "__lmod__", "__rmod__", "__mod__")

def eval_exp(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the exponentiation operator ('**')."""
    return _eval_binary_operation(lhs, rhs, env,"__lexp__", "__rexp__", "__exp__")

def eval_concat(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the string concatenation operator ('..')."""
    return _eval_binary_operation(lhs, rhs, env, "__lconcat__", "__rconcat__", "__concat__")

def eval_matmul(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the matrix multiplication operator ('@')."""
    return _eval_binary_operation(lhs, rhs, env, "__lmatmul__", "__rmatmul__", "__matmul__")

def eval_and(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the logical AND operator ('&&' / 'and')."""
    return _eval_binary_operation(lhs, rhs, env, "__land__", "__rand__", "__and__")

def eval_or(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the logical OR operator ('||' / 'or')."""
    return _eval_binary_operation(lhs, rhs, env, "__lor__", "__ror__", "__or__")

def eval_xor(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """Process operations using the logical XOR operator ('^^' / 'xor')."""
    return _eval_binary_operation(lhs, rhs, env, "__lxor__", "__rxor__", "__xor__")

def eval_sps(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.NumberValue:
    """Process operations using the spaceship operator ('<=>').

    Must return a Number."""
    return typing.cast(
        values.NumberValue,
        _eval_binary_operation(
            lhs, rhs, env,
            "__lsps__", "__rsps__", "__sps__",
            lambda x: isinstance(x, values.NumberValue)
        )
    )

def eval_lt(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """
    Process operations using the less operator ('<').
    The checking process is as follows, from top to bottom:
    - Run lhs's __lt__(other)
    - Run rhs's __gt__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, env, "__lt__", "__gt__")
    except:
        return values.BoolValue(eval_sps(lhs, rhs, env).value < 0)

def eval_gt(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """
    Process operations using the greater operator ('>').
    The checking process is as follows, from top to bottom:
    - Run lhs's __gt__(other)
    - Run rhs's __lt__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, env, "__gt__", "__lt__")
    except:
        return values.BoolValue(eval_sps(lhs, rhs, env).value > 0)

def eval_le(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """
    Process operations using the less-or-equal operator ('<=').
    The checking process is as follows, from top to bottom:
    - Run lhs's __le__(other)
    - Run rhs's __ge__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, env, "__le__", "__ge__")
    except:
        return values.BoolValue(eval_sps(lhs, rhs, env).value <= 0)

def eval_ge(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """
    Process operations using the greater-or-equal operator ('>=').
    The checking process is as follows, from top to bottom:
    - Run lhs's __le__(other)
    - Run rhs's __ge__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, env, "__ge__", "__le__")
    except:
        return values.BoolValue(eval_sps(lhs, rhs, env).value >= 0)

def eval_eq(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """
    Process operations using the less operator ('==').
    The checking process is as follows, from top to bottom:
    - Run lhs's __lt__(other)
    - Run rhs's __gt__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, env, "__eq__", "__eq__")
    except:
        return values.BoolValue(eval_sps(lhs, rhs, env).value == 0)

def eval_ne(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    """
    Process operations using the less operator ('<').
    The checking process is as follows, from top to bottom:
    - Run lhs's __lt__(other)
    - Run rhs's __gt__(other)
    - Run eval_sps(lhs, rhs)
    """
    try:
        return _eval_binary_operation(lhs, rhs, env, "__ne__", "__ne__")
    except:
        return values.BoolValue(eval_sps(lhs, rhs, env).value != 0)

# def eval_increment(expr: values.RuntimeValue) -> values.RuntimeValue:
#     """
#     Process operations using the increment operator ('++').
#     The checking is as follows, from top to bottom:
#     - Run expr.__incre__()
#     - Run expr.__iadd__(1), which, by itself, will call __add__, __ladd__ and __radd__ as fallback
#     """
#     from runtime.eval.inplaceops import eval_iadd
#     incre_fn: typing.Callable[[], values.RuntimeValue] | None = expr.__sap_props__.get("__incre__")
#     if callable(incre_fn):
#         val = incre_fn()
#         if val is not values.NOT_IMPLEMENTED:
#             return val
#     return eval_iadd(expr, values.Int(1))

# def eval_decrement(expr: values.RuntimeValue) -> values.RuntimeValue:
#     """
#     Process operations using the decrement operator ('--').
#     The checking is as follows, from top to bottom:
#     - Run expr.__decre__()
#     - Run expr.__isub__(1), which, by itself, will call __sub__, __lsub__ and __rsub__ as fallback
#     """
#     from runtime.eval.inplaceops import eval_isub
#     decre_fn: typing.Callable[[], values.RuntimeValue] | None = expr.__sap_props__.get("__decre__")
#     if callable(decre_fn):
#         val = decre_fn()
#         if val is not values.NOT_IMPLEMENTED:
#             return val
#     return eval_isub(expr, values.Int(1))

def eval_binaryand(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    return _eval_binary_operation(
        lhs, rhs, env, "__lbinand__", "__rbinand__", "__binand__"
    )

def eval_binaryor(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    return _eval_binary_operation(
        lhs, rhs, env, "__lbinor__", "__rbinor__", "__binor__"
    )

def eval_binaryxor(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    return _eval_binary_operation(
        lhs, rhs, env, "__lbinxor__", "__rbinxor__", "__binxor__"
    )

def eval_lshift(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    return _eval_binary_operation(
        lhs, rhs, env, "__llshift__", "__rlshift__", "__lshift__",
    )

def eval_rshift(lhs: values.RuntimeValue, rhs: values.RuntimeValue, env: env.Env) -> values.RuntimeValue:
    return _eval_binary_operation(
        lhs, rhs, env, "__lrshift__", "__rrshift__", "__rshift__",
    )