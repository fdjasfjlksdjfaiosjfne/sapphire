import parser.nodes as N
import runtime.values as V
from runtime.values import ValueType
from runtime.env import Environment

def eval_add(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num + num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value + rhs.value
        if isinstance(result, float): 
            return V.FloatVal(result)
        return V.IntVal(result)


def eval_sub(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num - num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value - rhs.value
        if isinstance(result, float): 
            return V.FloatVal(result)
        return V.IntVal(result)

def eval_mul(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num * num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value * rhs.value
        if isinstance(result, float): 
            return V.FloatVal(result)
        return V.IntVal(result)

def eval_div(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num / num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value / rhs.value
        if isinstance(result, float): 
            return V.FloatVal(result)
        return V.IntVal(result)

def eval_mod(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num % num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value % rhs.value
        if isinstance(result, float): 
            return V.FloatVal(result)
        return V.IntVal(result)

def eval_exp(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num ** num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value ** rhs.value
        if isinstance(result, float):
            return V.FloatVal(result)
        return V.IntVal(result)

def eval_lt(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num < num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value < rhs.value
        
        if result:
            return V.BoolVal(True)
        return V.BoolVal(False)

def eval_gt(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num > num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value > rhs.value
        
        if result:
            return V.BoolVal(True)
        return V.BoolVal(False)

def eval_le(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num <= num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value <= rhs.value
        
        if result:
            return V.BoolVal(True)
        return V.BoolVal(False)

def eval_ge(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num >= num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value >= rhs.value
        
        if result:
            return V.BoolVal(True)
        return V.BoolVal(False)

def eval_eq(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num == num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value == rhs.value
        
        if result:
            return V.BoolVal(True)
        return V.BoolVal(False)

def eval_ne(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num != num
    if ValueType.Number @ [lhs, rhs]:
        result = lhs.value != rhs.value
        
        if result:
            return V.BoolVal(True)
        return V.BoolVal(False)

def eval_spaceship(lhs: V.RuntimeVal, rhs: V.RuntimeVal, env: Environment) -> V.RuntimeVal:
    # num <=> num
    if ValueType.Number @ [lhs, rhs]:
        if lhs.value < rhs.value:
            return V.IntVal(-1)
        if lhs.value == rhs.value:
            return V.IntVal(0)
        return V.IntVal(1)