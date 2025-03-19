from parser.nodes import *
from runtime.values import *
from runtime.env import Environment

def eval_add(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num + num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value + rhs.value
        if isinstance(result, float): 
            return FloatVal(result)
        return IntVal(result)


def eval_sub(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num - num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value - rhs.value
        if isinstance(result, float): 
            return FloatVal(result)
        return IntVal(result)

def eval_mul(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num * num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value * rhs.value
        if isinstance(result, float): 
            return FloatVal(result)
        return IntVal(result)

def eval_div(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num / num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value / rhs.value
        if isinstance(result, float): 
            return FloatVal(result)
        return IntVal(result)

def eval_mod(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num % num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value % rhs.value
        if isinstance(result, float): 
            return FloatVal(result)
        return IntVal(result)

def eval_exp(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num ** num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value ** rhs.value
        if isinstance(result, float):
            return FloatVal(result)
        return IntVal(result)

def eval_lt(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num < num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value < rhs.value
        
        if result:
            return BoolVal(True)
        return BoolVal(False)

def eval_gt(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num > num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value > rhs.value
        
        if result:
            return BoolVal(True)
        return BoolVal(False)

def eval_le(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num <= num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value <= rhs.value
        
        if result:
            return BoolVal(True)
        return BoolVal(False)

def eval_ge(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num >= num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value >= rhs.value
        
        if result:
            return BoolVal(True)
        return BoolVal(False)

def eval_eq(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num == num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value == rhs.value
        
        if result:
            return BoolVal(True)
        return BoolVal(False)

def eval_ne(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num != num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value != rhs.value
        
        if result:
            return BoolVal(True)
        return BoolVal(False)

def eval_spaceship(lhs: RuntimeVal, rhs: RuntimeVal, env: Environment) -> RuntimeVal:
    # num <=> num
    if ValueType.Number @ [lhs, rhs]:
        if lhs.value < rhs.value:
            return IntVal(-1)
        if lhs.value == rhs.value:
            return IntVal(0)
        return IntVal(1)