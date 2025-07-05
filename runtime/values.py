from __future__ import annotations
import typing
from backend import errors

class RuntimeValMeta(type):
    """Metaclass for runtime values with special method handling."""
    registry: set = set()
    
    def __new__(mcls: RuntimeValMeta, 
                cls_name: str, 
                bases: tuple[type, ...], 
                namespace: dict[str, typing.Any]) -> typing.Any:
        
        new_dct = {}
        namespace.setdefault("sap_props", new_dct)

        # Grab annotations from the class being created
        annotations = namespace.get("__annotations__", {})

        # Dynamically injected __init__
        def __init__(self, *args, **kwargs):
            occupied = {"sap_props"}
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
            for base in bases:
                if hasattr(base, "sap_props") and isinstance(base.sap_props, dict):
                    # $ namespace["sap_props"] |= base.sap_props wouldn't work
                    # $ I want base.sap_props to fill in spots that 
                    # $ namespace["sap_props"] doesn't have.
                    # $ That code above did the complete opposite
                    # $ Would be funny if you can simplify this down to:
                    # namespace["sap_props"] =| base.sap_props
                    namespace["sap_props"] = base.sap_props | namespace["sap_props"]

            if "__init__" not in namespace or namespace["__init__"] is typing._overload_dummy:
                namespace["__init__"] = __init__
            namespace.setdefault("__eq__", __eq__)
            namespace.setdefault("__ne__", __ne__)
            namespace.setdefault("__slots__", tuple(annotations.keys()))

        return super().__new__(mcls, cls_name, bases, namespace)

def dunder_dict(fn):
    """Collect all methods from a function and return them as a dict.

Well...sort of.

The functions that is attached with this decorator is expected to return its local scope using `locals()`.

So this, quite literally, just replace the decorated function with its return value.

```
@dunder_dict
def sap_props():
    def foo():
        return 37
    return locals()

print(sap_props.foo()) # 37
```
    """
    return fn()

def try_dunder_coerce(obj, method_name: str, expected_type):
    if (
        hasattr(obj, "sap_props")
        and isinstance(obj.sap_props, dict)
        and method_name in obj.sap_props
        and callable(obj.sap_props[method_name])
    ):
        result = obj.sap_props[method_name]()
        if isinstance(result, expected_type):
            return result
        return None

class RuntimeVal(metaclass = RuntimeValMeta):
    """Base class for all runtime values in the Sapphire language."""
    def sap_props():
        def __or__(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
            if Bool(self if right else other).value:
                return self if right else other
            return other if right else self
        
        def __and__(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
            if not Bool(self if right else other).value:
                return self if right else other
            return other if right else self
        
        def __xor__(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
            if Bool(self).value != Bool(other).value:
                # & I could've just use '__or__()' here, but...
                # & Duck typing can broke __xor__ if __or__ is not handled correctly
                # ~ So I'm probably better off copy the code from __or__ instead for absolute certainty
                if Bool(self if right else other).value:
                    return self if right else other
                return other if right else self
            return Bool(False)
        
        def __not__(self) -> RuntimeVal:
            return Bool(not Bool(self.value))
        
        def __bool__(self) -> Bool: return Bool(True)



        return locals()

class Number(RuntimeVal):
    """Base class for numeric types."""
    def sap_props():
        def __add__(self, other: Number, right: bool) -> Number:
            if isinstance(other, (Int, Float)):
                val = self.value + other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NOT_IMPLEMENTED()
        
        def __sub__(self, other: Number, right: bool) -> Number:
            if isinstance(other, (Int, Float)):
                if right:
                    val = other.value - self.value
                else:
                    val = self.value - other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NOT_IMPLEMENTED()

        def __mul__(self, other: Number, right: bool) -> Number:
            if isinstance(other, (Int, Float)):
                val = self.value * other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NOT_IMPLEMENTED()

        def __truediv__(self, other: Number, right: bool) -> Number:
            if isinstance(other, (Int, Float)):
                if right:
                    val = other.value / self.value
                else:
                    val = self.value / other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NOT_IMPLEMENTED()

        def __floordiv__(self, other: Number, right: bool) -> Number:
            if isinstance(other, (Int, Float)):
                if right:
                    val = other.value // self.value
                else:
                    val = self.value // other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NOT_IMPLEMENTED()
        
        
        def __mod__(self, other: Number, right: bool) -> Number:
            if isinstance(other, (Int, Float)):
                if right:
                    val = other.value % self.value
                else:
                    val = self.value % other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NOT_IMPLEMENTED()
        
        
        def __sps__(self, other: Number) -> Int:
            if isinstance(other, (Int, Float)):
                if self.value < other.value:
                    return Int(-1)
                if self.value > other.value:
                    return Int(1)
                return Int(0)
            return NOT_IMPLEMENTED()

        def __str__(self) -> Str:
            return Str(self.value)

        def __repr__(self) -> Str:
            return Str(self.value)

        return locals()

class Int(Number):
    value: int
    
    def __init__(self, value): 
        if isinstance(value, int):
            self.value = value
        elif (coerced := try_dunder_coerce(value, "__int__", Int)):
            self.value = coerced.value
        else:
            raise errors.TypeError(f"{value!r} cannot be used")

    @dunder_dict
    def sap_props():
        def __binand__(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
            if isinstance(other, Int):
                return self.value & other.value
            return NOT_IMPLEMENTED()
        
        def __binor__(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
            if isinstance(other, Int):
                return self.value | other.value
            return NOT_IMPLEMENTED()
        
        def __binxor__(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
            if isinstance(other, Int):
                return self.value ^ other.value
            return NOT_IMPLEMENTED()

        return locals()

class Float(Number):
    value: float
    def __init__(self, value): 
        if isinstance(value, float):
            self.value = value
        elif (coerced := try_dunder_coerce(value, "__float__", Float)):
            self.value = coerced.value
        else:
            raise errors.TypeError(f"{value!r} cannot be used")
    @dunder_dict
    def sap_props():
        return locals()

class Str(RuntimeVal):
    value: str
    def __init__(self, value): 
        if isinstance(value, str):
            self.value = value
        elif (coerced := try_dunder_coerce(value, "__str__", Str)):
            self.value = coerced.value
        else:
            raise errors.TypeError(f"{value!r} cannot be used")
    @dunder_dict
    def sap_props():
        def __concat__(self, other: Str, right: bool) -> Str:
            if isinstance(other, Str):
                if right:
                    return Str(other.value + self.value)
                return Str(self.value + other.value)
            return NOT_IMPLEMENTED()
        
        
        def __lmul__(self, other: Int) -> Str:
            if isinstance(other, Int):
                return Str(self.value * other.value)
            return NOT_IMPLEMENTED()
        
        
        def __str__(self):
            return str(self.value)

        
        def __repr__(self):
            return repr(self.value)
        return locals()

class Bool(RuntimeVal):
    value: bool
    def __init__(self, value): 
        if isinstance(value, bool):
            self.value = value
        elif (coerced := try_dunder_coerce(value, "__bool__", Bool)):
            self.value = coerced.value
        else:
            raise errors.TypeError(f"{value!r} cannot be converted to a boolean")
    def sap_props():
        __binand__ = super().sap_props["__and__"]
        __binor__ = super().sap_props["__or__"]
        __binxor__ = super().sap_props["__xor__"]
        def __str__(self):
            return str(self.value).lower()
        def __repr__(self):
            return str(self.value).lower()
        return locals()

class Null(RuntimeVal):
    def sap_props():
        def __str__(self):
            return "null"
        def __repr__(self):
            return "null"
        return locals()

# I have to name it like this so that Python's NotImplemented is still usable
class NOT_IMPLEMENTED(RuntimeVal):
    @dunder_dict
    def sap_props():
        def __str__(self):
            return "NotImplemented"
        def __repr__(self):
            return "NotImplemented"
        return locals()

class List(RuntimeVal):
    value: list[RuntimeVal]
    def __init__(self, iterable = None, /):
        if isinstance(iterable, None):
            self.value = []
        elif isinstance(iterable, (list, tuple, set)):
            self.value = list(iterable)
        elif (coerced := try_dunder_coerce(iterable, "__list__", List)):
            self.value = coerced.value
        else:
            raise errors.TypeError(f"{iterable!r} cannot be used")
    
    @dunder_dict
    def sap_props():
        def append(self, object, /) -> Null:
            self.value.append(object)
            return Null()
        
        def insert(self, index, object, /) -> Null:
            self.value.insert(index, object)
            return Null()

        def __list__(self):
            return self
        def __tuple__(self):
            return Tuple()

class Tuple(RuntimeVal):
    value: list[RuntimeVal]
    def __init__(self, iterable = None, /):
        if isinstance(iterable, None):
            self.value = []
        elif isinstance(iterable, (list, tuple, set)):
            self.value = list(iterable)
        elif (coerced := try_dunder_coerce(iterable, "__tuple__", Tuple)):
            self.value = coerced.value
        else:
            raise errors.TypeError(f"{iterable!r} cannot be used")

class Argument(typing.NamedTuple):
    name: str
    kind: typing.Literal["Pos", "PosKey", "Key", "*", "**"]
    default: RuntimeVal | None = None # type: ignore
    hint: typing.Any = None # todo add type hint support

class NativeFn(RuntimeVal):
    @typing.overload
    def __init__(self, arguments: list[Argument], caller: typing.Callable[..., RuntimeVal], return_hint) -> None: ...
    arguments: list[Argument]
    caller: typing.Callable[..., RuntimeVal]
    return_hint: typing.Any
    def __call__(self, *args: RuntimeVal, **kwargs: RuntimeVal):
            return self.caller(*args, **kwargs)
    def sap_props():
        def __call__(self, *args: RuntimeVal, **kwargs: RuntimeVal):
            return self.caller(*args, **kwargs)
        return locals()
    def bind(self, instance):
        return NativeFn(
            self.arguments[1:],
            lambda *args, **kwargs: self.caller.sap_props["__call__"](instance, *args, **kwargs)
        )