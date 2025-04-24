from __future__ import annotations
import typing
from runtime.env import Env

class RuntimeVal:
    def __init_subclass__(cls):
        def __init__(self, *args, **kwargs):
            occupied = []
            for name, arg in zip(cls.__annotations__.keys(), args):
                occupied.append(name)
                setattr(self, name, arg)
            
            for k, v in kwargs.items():
                if k in occupied:
                    raise ValueError("...")
                setattr(self, k, v)
        
        if not hasattr(cls, "__init__"):
            cls.__init__ = __init__

    def __eq__(self, other):
        if hasattr(self, "value"): 
            return self.value == other
        return NotImplemented
    
    def __ne__(self, other):
        if hasattr(self, "value"):
            return self.value != other
        return NotImplemented

class Number(RuntimeVal): # Add this base class for numbers
    def __instancecheck__(self, instance: typing.Any) -> bool:
        return isinstance(instance, (Int, Float)) # 👍
    def __repr__(self):
        return str(self.value)

class Int(Number):
    def __init__(self, value: int):
        self.value = value

class Float(Number):
    def __init__(self, value: float):
        self.value = value

class Str(RuntimeVal):
    def __init__(self, value: str):
        self.value = value
    def __repr__(self):
        return self.value


class Bool(RuntimeVal):
    def __init__(self, value: bool):
        self.value = value
    def __repr__(self):
        return str(self.value).lower()


class Null(RuntimeVal):
    def __init__(self):
        self.value = None
    def __repr__(self):
        return "null"


class NotImplemented(RuntimeVal):
    def __repr__(self):
        return "NotImplemented"


class NativeFn(RuntimeVal):
    pass

RuntimeVals = typing.Union [
    Int,
    Float,
    Str,
    Bool,
    Null,
    NativeFn
]