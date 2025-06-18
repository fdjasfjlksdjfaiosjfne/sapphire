from __future__ import annotations
import typing
class RuntimeValMeta(type):
    """Metaclass for runtime values with special method handling."""
    registry: set = set()
    
    def __new__(mcls: RuntimeValMeta, 
                cls_name: str, 
                bases: tuple[type, ...], 
                namespace: dict[str, typing.Any]) -> typing.Any:
        
        # Safe per-class dunder map
        dunders = {}
        namespace["__sap_props__"] = dunders

        # Grab annotations from the class being created
        annotations = namespace.get("__annotations__", {})

        # Dynamically injected __init__
        def __init__(self, *args, **kwargs):
            occupied = {"__sap_props__"}
            for name, arg in zip(annotations.keys(), args):
                occupied.add(name)
                setattr(self, name, arg)
            for k, v in kwargs.items():
                if k in occupied:
                    raise ValueError(f"Argument {k} is being defined both in a positional and keyword manner.")
                setattr(self, k, v)

        # Equality helpers
        def __eq__(self, other):
            if isinstance(other, tuple(mcls.registry)) and hasattr(other, "value"):
                return self.value == other
            return NotImplemented

        def __ne__(self, other):
            if isinstance(other, tuple(mcls.registry)) and hasattr(other, "value"):
                return self.value != other
            return NotImplemented

        mcls.registry.add(mcls)

        if cls_name != "RuntimeVal":
            to_delete = []
            # ? Scrolling through the items to find 
            for name, val in namespace.items():
                if callable(val) and hasattr(val, "__sap_dunder_name"):
                    dunders[getattr(val, "__sap_dunder_name")] = val
                    to_delete.append(name)
            for name in to_delete:
                del namespace[name]

            namespace.setdefault("__init__", __init__)
            namespace.setdefault("__eq__", __eq__)
            namespace.setdefault("__ne__", __ne__)
            namespace.setdefault("__slots__", tuple(annotations.keys()))

        return super().__new__(mcls, cls_name, bases, namespace)

def sap_dunder(fn: typing.Callable, name: typing.Optional[str | list[str]] = None):
    if name is None:
        name = f"__{fn.__name__}__"
    
    setattr(fn, "__sap_dunder_name", name)
    return fn

class RuntimeVal(metaclass = RuntimeValMeta):
    """Base class for all runtime values in the Sapphire language."""

class Number(RuntimeVal):
    """Base class for numeric types."""

class Int(Number):
    value: int
    
    @sap_dunder
    def add(self, other: Number, right: bool) -> Number:
        if isinstance(other, Int):
            return Int(self.value + other.value)
        elif isinstance(other, Float):
            return Float(self.value + other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def sub(self, other: Number, right: bool) -> Number:
        if isinstance(other, Int):
            if right:
                return Int(other.value - self.value)
            return Int(self.value - other.value)
        elif isinstance(other, Float):
            if right:
                return Float(other.value - self.value)
            return Float(self.value - other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def mul(self, other: Number, right: bool) -> Number:
        if isinstance(other, Int):
            return Int(self.value * other.value)
        elif isinstance(other, Float):
            return Float(self.value * other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def truediv(self, other: Number, right: bool) -> Number:
        if isinstance(other, (Int, Float)):
            if right:
                return Float(other.value / self.value)
            return Float(self.value / other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def floordiv(self, other: Number, right: bool) -> Number:
        if isinstance(other, (Int, Float)):
            if right:
                return Int(other.value // self.value)
            return Int(self.value // other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def mod(self, other: Number, right: bool) -> Number:
        if isinstance(other, (Int, Float)):
            if right:
                return Int(other.value % self.value)
            return Int(self.value % other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def sps(self, other: Number) -> Int:
        if isinstance(other, (Int, Float)):
            if self.value < other.value:
                return Int(-1)
            if self.value > other.value:
                return Int(1)
            return Int(0)
        return NOT_IMPLEMENTED()

    @sap_dunder
    def str(self):
        return self.value

    @sap_dunder
    def repr(self):
        return repr(self.value)

class Float(Number):
    value: float
    
    @sap_dunder
    def add(self, other: Number, right: bool) -> Number:
        if isinstance(other, (Int, Float)):
            return Float(self.value + other.value)
        return NOT_IMPLEMENTED()

    @sap_dunder
    def sub(self, other: Number, right: bool) -> Number:
        if isinstance(other, (Int, Float)):
            if right:
                return Float(other.value - self.value)
            return Float(self.value - other.value)
        return NOT_IMPLEMENTED()

    @sap_dunder
    def add(self, other: Number, right: bool) -> Number:
        if isinstance(other, (Int, Float)):
            return Float(self.value * other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def truediv(self, other: Number, right: bool) -> Number:
        if isinstance(other, (Int, Float)):
            if right:
                return Float(other.value / self.value)
            return Float(self.value / other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def floordiv(self, other: Number, right: bool) -> Number:
        if isinstance(other, (Int, Float)):
            if right:
                return Int(other.value // self.value)
            return Int(self.value // other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def mod(self, other: Number, right: bool) -> Number:
        if isinstance(other, (Int, Float)):
            if right:
                return Int(other.value % self.value)
            return Int(self.value % other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def sps(self, other: Number) -> Int:
        if isinstance(other, (Int, Float)):
            if self.value < other.value:
                return Int(-1)
            if self.value > other.value:
                return Int(1)
            return Int(0)
        return NOT_IMPLEMENTED()

    @sap_dunder
    def str(self):
        return str(self.value)

    @sap_dunder
    def repr(self):
        return repr(self.value)

class Str(RuntimeVal):
    value: str
    
    @sap_dunder
    def concat(self, other: Str, right: bool) -> Str:
        if isinstance(other, Str):
            if right:
                return Str(other.value + self.value)
            return Str(self.value + other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def lmul(self, other: Int) -> Str:
        if isinstance(other, Int):
            return Str(self.value * other.value)
        return NOT_IMPLEMENTED()
    
    @sap_dunder
    def str(self):
        return str(self.value)

    @sap_dunder
    def repr(self):
        return repr(self.value)

class Bool(RuntimeVal):
    value: bool
    @sap_dunder
    def str(self):
        return str(self.value).lower()

    @sap_dunder
    def repr(self):
        return str(self.value).lower()

class Null(RuntimeVal):
    @sap_dunder
    def repr(self):
        return "null"

# I have to name it like this so that Python's NotImplemented is still usable
class NOT_IMPLEMENTED(RuntimeVal):
    @sap_dunder
    def str(self):
        return "NotImplemented"

    @sap_dunder
    def repr(self):
        return "NotImplemented"

NoDefault = object()
class Argument(typing.NamedTuple):
    name: str
    kind: typing.Literal["Pos", "PosKey", "Key", "*", "**"]
    default: RuntimeVal | NoDefault # type: ignore
    hint: typing.Any        # ~ temp

class NativeFn(RuntimeVal):
    arguments: list[Argument]
    caller: typing.Callable[..., RuntimeVal]
    return_hint: typing.Any