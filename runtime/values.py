from __future__ import annotations
import types
import typing
import inspect

from backend import errors
from parser import nodes



def convert_to_runtime_val(val) -> RuntimeVal:
    if isinstance(val, RuntimeVal):
        return val
    if isinstance(val, int):
        return Int(val)
    if isinstance(val, float):
        return Float(val)
    if isinstance(val, str):
        return Str(val)
    if isinstance(val, bool):
        return Bool(val)
    if val is None:
        return Null()
    if val is NotImplemented:
        return NotImplemented_
    if isinstance(val, list):
        return List(val)
    if isinstance(val, tuple):
        return Tuple(val)
    from parser.nodes import BaseNode
    if isinstance(val, BaseNode):
        raise errors.InternalError(
            "Hey man. What if, just what if, just use evaluate() " \
            "from runtime/interperter.py? WHAT THE FUCK IS WRONG WITH " \
            "YOU? ARE YOU FUCKING STUPID? IT'S THERE FOR A REASON. " \
            "In case you're just a user, this is just me (and perhaps " \
            "this codebase too) having a existential crisis, nothing to " \
            "worry about here :^)"
        )
    raise errors.InternalError(
        f"Incompatible value passed into convert() in runtime/values.py ({val!r} of type {type(val)})"
    )

class RuntimeValMeta(type):
    """Metaclass for runtime values with special method handling."""
    registry: set = set()
    def __new__(mcls: type[RuntimeValMeta], 
                cls_name: str, 
                bases: tuple[type, ...], 
                namespace: dict[str, typing.Any]) -> typing.Any:
        
        new_dct = {}
        namespace.setdefault("attributes", new_dct)

        # Grab annotations from the class being created
        annotations = namespace.get("__annotations__", {})

        # Dynamically injected __init__
        def __init__(self, *args, **kwargs):
            occupied = {"attributes"}
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
            return NotImplemented_

        def __ne__(self, other):
            if isinstance(other, tuple(mcls.registry)) and hasattr(other, "value"):
                return self.value != other
            return NotImplemented_

        mcls.registry.add(cls_name)

        if cls_name != "RuntimeVal":
            for base in bases:
                if hasattr(base, "attributes") and isinstance(base.attributes, dict):
                    # $ namespace["attributes"] |= base.attributes wouldn't work
                    # $ I want base.attributes to fill in spots that 
                    # $ namespace["attributes"] doesn't have.
                    # $ That code above did the complete opposite
                    # $ Would be funny if you can simplify this down to:
                    # namespace["attributes"] =| base.attributes
                    namespace["attributes"] = base.attributes | namespace["attributes"]

            # $ You can't directly access typing._overload_dummy without Pylance yelling at you
            # * Just call typing.overload(), which returns typing._overload_dummy
            # ~ ***Might*** be brittle

            if (namespace.get("__init__", None) is None or 
                namespace["__init__"] is typing.overload(lambda: None) or
                namespace["__init__"] is pls_dont_call_me):
                namespace["__init__"] = __init__
            namespace.setdefault("__eq__", __eq__)
            namespace.setdefault("__ne__", __ne__)
            namespace.setdefault("__slots__", tuple(annotations.keys()))
        return super().__new__(mcls, cls_name, bases, namespace)

def pls_dont_call_me(*_: typing.Never, **__: typing.Never) -> typing.Never:
    raise errors.InternalError(
        "This method was marked with @begone and "
        "should never be called. If it does called, "
        "RuntimeValMeta.__new__() is probably faulty"
    )

def begone[F](fn: F) -> F:
    """Mark a method for deletion while preserving its type signature."""
    return typing.cast(F, pls_dont_call_me)

def attribute_dict(fn) -> dict[str, RuntimeVal | typing.Callable]:
    """Collect all methods from a function and return them as a dict.

Well...sort of.

The functions that is attached with this decorator is expected to return its local scope using `locals()`.

So this, quite literally, just replace the decorated function with its return value.

```
@dunder_dict
def attributes():
    def foo():
        return 37
    return locals()

print(attributes.foo()) # 37
```
    """
    return fn()

def try_dunder_coerce(obj, method_name: str, expected_type):
    if (hasattr(obj, "attributes")
            and isinstance(obj.attributes, dict)
            and method_name in obj.attributes
            and callable(obj.attributes[method_name])):
        result = obj.attributes[method_name]()
        if isinstance(result, expected_type):
            return result
        return None

class RuntimeVal(metaclass = RuntimeValMeta):
    attributes: dict[str, RuntimeVal | typing.Callable]

class Object(RuntimeVal):
    """Base class for all runtime values in the Sapphire language."""
    
    @attribute_dict
    def attributes():
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

        def __getattribute__(self, attr):
            if attr in self.attributes:
                return self.attributes[attr]
            raise errors.AttributeError(f"Unable to find attribute '{attr}' in object")

        return locals()

class Number(Object):
    """Base class for numeric types."""
    @begone
    def __init__(self, value: int | float): ...
    @attribute_dict
    def attributes():
        def __add__(self, other: Number, right: bool) -> RuntimeVal:
            if isinstance(other, (Int, Float)):
                val = self.value + other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NotImplemented_
        
        def __sub__(self, other: Number, right: bool) -> RuntimeVal:
            if isinstance(other, (Int, Float)):
                if right:
                    val = other.value - self.value
                else:
                    val = self.value - other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NotImplemented_

        def __mul__(self, other: Number, right: bool) -> RuntimeVal:
            if isinstance(other, (Int, Float)):
                val = self.value * other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NotImplemented_

        def __truediv__(self, other: Number, right: bool) -> RuntimeVal:
            if isinstance(other, (Int, Float)):
                if right:
                    val = other.value / self.value
                else:
                    val = self.value / other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NotImplemented_

        def __floordiv__(self, other: Number, right: bool) -> RuntimeVal:
            if isinstance(other, (Int, Float)):
                if right:
                    val = other.value // self.value
                else:
                    val = self.value // other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NotImplemented_
        
        
        def __mod__(self, other: Number, right: bool) -> RuntimeVal:
            if isinstance(other, (Int, Float)):
                if right:
                    val = other.value % self.value
                else:
                    val = self.value % other.value
                val = typing.cast(int | float, val)
                if isinstance(val, Int):
                    return Int(val)
                return Float(val)
            return NotImplemented_
        
        
        def __sps__(self, other: Number) -> RuntimeVal:
            if isinstance(other, (Int, Float)):
                if self.value < other.value:
                    return Int(-1)
                if self.value > other.value:
                    return Int(1)
                return Int(0)
            return NotImplemented_

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

    @attribute_dict
    def attributes():
        def __binand__(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
            if isinstance(other, Int):
                return self.value & other.value
            return NotImplemented_
        
        def __binor__(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
            if isinstance(other, Int):
                return self.value | other.value
            return NotImplemented_
        
        def __binxor__(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
            if isinstance(other, Int):
                return self.value ^ other.value
            return NotImplemented_

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
    @attribute_dict
    def attributes():
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
    @attribute_dict
    def attributes():
        def __concat__(self, other: Str, right: bool) -> Str:
            if isinstance(other, Str):
                if right:
                    return Str(other.value + self.value)
                return Str(self.value + other.value)
            return NotImplemented_
        
        def __lmul__(self, other: Int) -> Str:
            if isinstance(other, Int):
                return Str(self.value * other.value)
            return NotImplemented_
        
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
    @attribute_dict
    def attributes():
        __binand__ = super().attributes["__and__"]
        __binor__ = super().attributes["__or__"]
        __binxor__ = super().attributes["__xor__"]
        def __str__(self):
            return str(self.value).lower()
        def __repr__(self):
            return str(self.value).lower()
        return locals()

true = Bool(True)
false = Bool(False)

class Null(RuntimeVal):
    @attribute_dict
    def attributes():
        def __str__(self):
            return "null"
        def __repr__(self):
            return "null"
        return locals()

null = Null()

class _Not_Implemented(RuntimeVal):
    pass

NotImplemented_ = _Not_Implemented()

class Class(RuntimeVal):
    @begone
    def __init__(
        self, 
        name: str, 
        base: Class | None, 
        methods: dict[str, 
                  RuntimeVal
                  | types.FunctionType
                  | types.BuiltinFunctionType
                  | staticmethod
                  | classmethod]): ...
    name: str
    base: Class | None
    methods: dict[str,
                  RuntimeVal
                  | types.FunctionType
                  | types.BuiltinFunctionType
                  | staticmethod
                  | classmethod]
    def resolve(self, name):
        if name in self.methods:
            return self.methods[name]
        if self.base:
            return self.base.resolve(name)
        return None

class Instance(RuntimeVal):
    def __init__(self, cls: Class):
        self.cls = cls
        self.fields: dict[str, RuntimeVal] = {}

    

    @typing.final
    def get_attribute(self, attr: str):
        if attr in self.fields:
            return self.fields[attr]
        if attr in self.cls.methods:
            meth = self.cls.methods

            # $ Wrap it in NativeFn if it is Python's function
            # $ If it's a Python function, it's probably a built-in
            # $ implementation of a class
            if isinstance(meth, 
                          (types.FunctionType, types.BuiltinFunctionType)):
                def translate_kind(k: inspect._ParameterKind):
                    match k:
                        case inspect._ParameterKind.POSITIONAL_ONLY:
                            return "Pos"
                        case inspect._ParameterKind.POSITIONAL_OR_KEYWORD:
                            return "PosKey"
                        case inspect._ParameterKind.KEYWORD_ONLY:
                            return "Key"
                        case inspect._ParameterKind.VAR_POSITIONAL:
                            return "*"
                        case inspect._ParameterKind.VAR_KEYWORD:
                            return "**"
                        case _:
                            raise errors.InternalError(
                                "Incorrect value enter into Instance.get_attribute()."
                                "translate_kind() from runtime/values.py." \
                                f"Expecting a inspect._ParameterKind enum value, got {k}"
                            )

                sig = inspect.signature(meth)
                args_annotation = sig.parameters
                args = [
                    Argument(name, translate_kind(arg.kind), arg.default)
                    for name, arg
                    in args_annotation.items()
                ]
                meth = NativeFn(args, meth)
                return meth.bind(self)
            elif isinstance(meth, (NativeFn, CustomFn)):
                return meth.bind(self)
            elif isinstance(meth, RuntimeVal):
                # & Whatever. Just accept a runtime value.
                return meth
            else:
                raise errors.AttributeError(f"{self.cls.name} has no attribute {attr}")



class List(RuntimeVal):
    value: list[RuntimeVal]
    def __init__(self, iterable = None, /):
        if iterable is None:
            self.value = []
        elif isinstance(iterable, (list, tuple, set)):
            self.value = list(iterable)
        elif (coerced := try_dunder_coerce(iterable, "__list__", List)):
            self.value = coerced.value
        else:
            raise errors.TypeError(f"{iterable!r} cannot be used")
        self.value = typing.cast(list[RuntimeVal], self.value)
        self.value.extend
    @attribute_dict
    def attributes():
        def append(self, object, /):
            self.value.append(object)
        
        def clear(self):
            self.value.clear()

        def insert(self, index, object, /):
            self.value.insert(index, object)

        def index(self, value, start = 0, stop = 0) -> Int | ValueError:
            try:
                return Int(self.value.index(value, start, stop))
            except ValueError:
                raise errors.ValueError(f"{value!r} does not exist in list")
        
        def copy(self) -> List:
            return List(self.value.copy())
        
        def count(self, value: RuntimeVal) -> Int:
            return Int(self.value.count(value))
        
        def extend(self, iterable):
            self.value.extend(iterable.attributes["__iter__"])

        def __list__(self):
            return self
        def __tuple__(self):
            return Tuple()
        return locals()

class Tuple(RuntimeVal):
    value: list[RuntimeVal]
    def __init__(self, iterable = None, /):
        if iterable is None:
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
    hint: typing.Any = None # todo add type hint support...

class NativeFn(RuntimeVal):
    @begone
    def __init__(self, arguments: list[Argument], 
                 caller: typing.Callable[..., RuntimeVal], 
                 return_hint = None): ...
    arguments: list[Argument]
    caller: typing.Callable[..., RuntimeVal]
    return_hint: typing.Any
    def __call__(self, *args: RuntimeVal, **kwargs: RuntimeVal):
        return self.caller(*args, **kwargs)
    
    @attribute_dict
    def attributes():
        def __call__(self, *args: RuntimeVal, **kwargs: RuntimeVal):
            return self.caller(*args, **kwargs)
        return locals()
    
    def bind(self, instance: Instance | Class) -> NativeFn:
        return NativeFn(
            self.arguments[1:],
            lambda *args, **kwargs: self.caller(instance, *args, **kwargs),
            self.return_hint
        )

class CustomFn(RuntimeVal):
    @begone
    def __init__(self, arguments: list[Argument], 
                 code: nodes.CodeBlockNode, 
                 return_hint = None): ...
    arguments: list[Argument]
    code: nodes.CodeBlockNode
    return_hint: typing.Any
    def __call__(self, *args: RuntimeVal, **kwargs: RuntimeVal):
        raise errors.InternalError(
            "In progress..."
        )
    
    @attribute_dict
    def attributes():
        ...
        return locals()
    
    def bind(self, instance: Instance | Class) -> NativeFn:
        raise errors.InternalError(
            "In progress..."
        )