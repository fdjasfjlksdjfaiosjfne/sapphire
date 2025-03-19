from __future__ import annotations
from parser.nodes import *
from enum import *

@unique
class ValueType(Enum):
    Unusable = auto()
    Int = auto()
    Float = auto()
    Number = auto() # Only used for comparisons
    Str = auto()
    Bool = auto()
    Null = auto()
    NativeFn = auto()
    Fn = auto()
    NotImplemented = auto()
    
    def __matmul__(self, runtime_vals: List[RuntimeVal]|Tuple[RuntimeVal]|Set[RuntimeVal]):
        return all([val == self for val in runtime_vals])

class RuntimeVal:
    kind: ValueType
    def __init_subclass__(cls):
        setattr(cls, "kind", getattr(ValueType, cls.__name__.removesuffix("Val")))

    def __eq__(self, comparing_kind):
        if isinstance(comparing_kind, ValueType):
            e = self.kind in {ValueType.Int, ValueType.Float} if comparing_kind == ValueType.Number else self.kind == comparing_kind
            return e
        if hasattr(self, "value"): 
            return self.value == comparing_kind
        return NotImplemented
    
    def __ne__(self, value):
        if hasattr(self, "value"): 
            return self.value != value
        return NotImplemented

@dataclass(eq = False)
class IntVal(RuntimeVal):
    value: int

@dataclass(eq = False)
class FloatVal(RuntimeVal):
    value: float

@dataclass(eq = False)
class StrVal(RuntimeVal):
    value: str

@dataclass(eq = False)
class BoolVal(RuntimeVal):
    value: bool

@dataclass(eq = False)
class NullVal(RuntimeVal): pass

@dataclass(eq = False)
class NativeFnVal(RuntimeVal):
    from runtime.env import Environment
    caller: Callable[[List[RuntimeVal], Environment], RuntimeVal]
    def __bool__(self):
        return True

@dataclass(eq = False)
class UnusableVal(RuntimeVal):
    """
    This class is used specifically for things that cannot be used as expressions (stmts, program's code blocks, etc)
    """

@dataclass(eq = False)
class NotImplementedVal(RuntimeVal): pass