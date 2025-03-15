from parser.nodes import *
from enum import *

@unique
class ValueType(Enum):
    Int = auto()
    Float = auto()
    Str = auto()
    Bool = auto()
    Null = auto()

class RuntimeVal:
    kind: ValueType
    def __init_subclass__(cls):
        setattr(cls, "kind", getattr(ValueType, cls.__name__.removesuffix("Val")))

@dataclass
class IntVal(RuntimeVal):
    value: int

@dataclass
class FloatVal(RuntimeVal):
    value: float

@dataclass
class StrVal(RuntimeVal):
    value: str

@dataclass
class BoolVal(RuntimeVal):
    value: bool

@dataclass
class NullVal(RuntimeVal): pass