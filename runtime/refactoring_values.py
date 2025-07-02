"""
A isolated version of values.py that attempts to refactor the entire object hierarchy for seamless OOP support.

Currently in a non-functional state.

Should not be used until the refactor is complete.
"""

from __future__ import annotations
import typing
import inspect
import builtins

from backend import errors
from runtime import native_fns
class RuntimeValMeta(type):
    """Metaclass for runtime values with special method handling."""
    registry: list = []
    
    def __new__(mcls: type[RuntimeValMeta],
                cls_name: str, 
                bases: tuple[type, ...], 
                namespace: dict[str, typing.Any]) -> typing.Any:

        # Safe per-class dunder map
        # dunders = {}
        # namespace["sap_props"] = dunders

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
        
        
        
        # # ^ Dunder methods that will inserted by default
        # @sap_dunder(add_extra_prop = False)
        # def __and__(self, other: RuntimeVal, right: bool) -> RuntimeVal:


        # @sap_dunder(add_extra_prop = False)
        # def __or__(self, other: RuntimeVal, right: bool) -> RuntimeVal:
        #     if native_fns.bool(self if right else other).value:
        #         return self if right else other
        #     return other if right else self
        
        # @sap_dunder(add_extra_prop = False)
        # def __xor__(self, other: RuntimeVal, right: bool) -> RuntimeVal:
        #     if native_fns.bool(self).value != native_fns.bool(other).value:
        #         # & I could've just use '__or__()' here, but...
        #         # & Duck typing can broke __xor__ if __or__ is not handled correctly
        #         # ~ So I'm probably better off copy the code from __or__ instead for absolute certainty
        #         if native_fns.bool(self if right else other).value:
        #             return self if right else other
        #         return other if right else self
        #     return Bool(False)
        
        # @sap_dunder(add_extra_prop = False)
        # def __not__(self) -> RuntimeVal:
        #     return Bool(not native_fns.bool(self).value)

        # mcls.registry.add(mcls)

        # if cls_name != "RuntimeVal":
        #     to_delete = []
        #     # ? Scrolling through the items to find 
        #     for name, val in namespace.items():
        #         if callable(val) and hasattr(val, "__sap_dunder_name"):
        #             for i in getattr(val, "__sap_dunder_name"):
        #                 i = typing.cast(str, i)
        #                 dunders[i] = val
        #             to_delete.append(name)
        #     for name in to_delete:
        #         del namespace[name]

        #     # Note: setdefault() only adds the pair if it doesn't exist alrady
            
        #     namespace.setdefault("__init__", __init__)
        #     namespace.setdefault("__eq__", __eq__)
        #     namespace.setdefault("__ne__", __ne__)
        #     namespace.setdefault("__slots__", tuple(annotations.keys()))

        #     # ^ Add certain dunders into `sap_prop` if it isn't there already
            
        #     namespace["sap_props"].setdefault("__and__", __and__)
        #     namespace["sap_props"].setdefault("__or__", __or__)
        #     namespace["sap_props"].setdefault("__xor__", __xor__)
        #     namespace["sap_props"].setdefault("__not__", __not__)

        #     # ^ Add the properties from the namespace to the type object
        #     type_obj: Type = namespace.get("type")
        #     if hasattr(type_obj, "sap_props") and isinstance(type_obj.sap_props, dict):
        #         # $ dict | dict will merge the two dicts together
        #         # $ In case the one who is reading this don't know or forgot
        #         type_obj.sap_props |= namespace["sap_props"]
        #     elif type_obj:
        #         setattr(type_obj, "sap_props", namespace["sap_props"])

        # return super().__new__(mcls, cls_name, bases, namespace)

def dunder_dict(fn):
    """Collect all methods from a function and return them as a dict.

    Well...sort of.

    The functions that is attached with this decorator is expected to return its local scope using `locals()`.

    So this, quite literally, just replace the decorated function with its return value.
    """
    return fn()

class RuntimeVal(metaclass = RuntimeValMeta):
    """Base class for all runtime values in the Sapphire language."""
    # ~ In reality, sap_props does not allow callables
    # ~ It's there just so static type checkers can sleep peacefully
    sap_props: dict[str, RuntimeVal] | typing.Callable
    base: Type

class Type(RuntimeVal):
    @dunder_dict
    def sap_props():
        def __new__(
                mcls: Type[Type], 
                name: Str, 
                bases: Tuple[type], 
                namespace: Dict[Str, typing.Any]):
            pass

class Object(Type):
    @dunder_dict
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

        def __str__(self) -> Str:
            return f"<{self.base} {self.__name__}>"

        return locals()

class Class(Object):
    def __init__(self, name: str, methods: dict[str, NativeCallable], base: Class | None):
        self.name = name
        self.methods = methods
        self.base = base

class Instance(Object):
    def __init__(self, cls: Class):
        self.cls = cls
        self.fields: dict[str, RuntimeVal] = {}
    
    def sap_props():
        def __getattribute__(self, name: str) -> RuntimeVal:
            # 1. Instance field
            if name in self.fields:
                return self.fields[name]
            # 2. Class methods
            if name in self.cls.methods:
                method = self.cls.methods[name]
                return method.bind(self)
            # 3. Inherited
            if self.cls.base is not None:
                return self.cls.base.sap_props["__getattribute__"](name)
        return locals()

class Int(Object):
    @dunder_dict
    def sap_props():
        return locals()

class Float(Object):
    @dunder_dict
    def sap_props():
        pass

class Bool(Object):
    pass

class Str(Object):
    pass

class Null(Object):
    pass

class List(Object):
    pass

class Tuple(Object):
    pass

class Set(Object):
    pass

class Dict(Object):
    pass

class FnArgument(typing.NamedTuple):
    """A wrapper to store argument data for NativeCallable and Callable data types."""
    name: str
    kind: typing.Literal["Pos", "PosKey", "Key", "*", "**"]
    default: typing.Optional[RuntimeVal] = None
    hint: typing.Any = None

class NativeCallable(Object):
    def __init__(self, name: str, arguments: list[FnArgument], caller: typing.Callable, return_hint: typing.Any):
        self.name = name
        self.arguments = arguments
        self.caller = caller
        self.return_hint = return_hint
    
    def bind(self, instance):
        

class Function(Object):
    pass

# class Type(RuntimeVal):

# class Type(RuntimeVal):
#     """Base class for built-in types."""
#     name: str

# INT_TYPE = Type("int")
# STR_TYPE = Type("str")
# FLOAT_TYPE = Type("float")
# BOOL_TYPE = Type("bool")
# NULL_TYPE = Type("NullType")
# NOT_IMPLEMENTED_TYPE = Type("NotImplementedType")
# NATIVE_CALLABLE_TYPE = Type("NativeCallableType")

# class Number(RuntimeVal):
#     """Base class for numeric types."""
#     value: int | float)
#     def __instancecheck__(self, instance) -> typing.TypeIs[Int | Float]: 
#         return isinstance(instance, (Int, Float))

# class Int(Number):
#     value: int
#     type = INT_TYPE

#     @sap_dunder
#     def add(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
#         if isinstance(other, Int):
#             return Int(self.value + other.value)
#         elif isinstance(other, Float):
#             return Float(self.value + other.value)
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def sub(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
#         if isinstance(other, Int):
#             if right.value:
#                 return Int(other.value - self.value)
#             return Int(self.value - other.value)
#         elif isinstance(other, Float):
#             if right.value:
#                 return Float(other.value - self.value)
#             return Float(self.value - other.value)
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def mul(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
#         if isinstance(other, Int):
#             return Int(self.value * other.value)
#         elif isinstance(other, Float):
#             return Float(self.value * other.value)
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def truediv(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
#         if isinstance(other, (Int, Float)):
#             if right.value:
#                 if self.value == 0:
#                     raise errors.ZeroDivisionError("Division by 0")
#                 return Float(other.value / self.value)
#             if other.value == 0: 
#                     raise errors.ZeroDivisionError("Division by 0")
#             return Float(self.value / other.value)
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def floordiv(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
#         if isinstance(other, Int):
#             if right.value:
                
#                 return Int(other.value // self.value)
#             return Int(self.value // other.value)
#         if isinstance(other, Float):
#             if right.value:
#                 return Float(other.value // self.value)
#             return Float(self.value // other.value)
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def mod(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
#         if isinstance(other, Int):
#             if right.value:
#                 return Int(other.value % self.value)
#             return Int(self.value % other.value)
#         if isinstance(other, Float):
#             if right.value:
#                 return Float(other.value % self.value)
#             return Float(self.value % other.value)
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def exp(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
#         if isinstance(other, Int):
#             if right.value:
#                 return Int(other.value ** self.value)
#             return Int(self.value, other.value)
#         if isinstance(other, Float):
#             if right.value:
#                 return Float(other.value ** self.value)
#             return Float(self.value ** other.value)
#         return NOT_IMPLEMENTED()

#     @sap_dunder
#     def sps(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
#         if isinstance(other, (Int, Float)):
#             if self.value < other.value:
#                 return Int(1 if right else -1) 
#             if self.value > other.value:
#                 return Int(-1 if right else 1)
#             return Int(0)
#         return NOT_IMPLEMENTED()

#     @sap_dunder(name = ["__and__", "__binand__"])
#     def and_(self, other: RuntimeVal, right: Bool) -> RuntimeVal:
#         if isinstance(other, Int):
#             return 
#         return NOT_IMPLEMENTED()


#     @sap_dunder
#     def str(self) -> Str:
#         return Str(str(self.value))

#     @sap_dunder
#     def int(self) -> Int:
#         return self
    
#     @sap_dunder
#     def float(self) -> Float:
#         return Float(self.value)

#     @sap_dunder
#     def repr(self) -> Str:
#         return Str(repr(self.value))
    
#     def __str__(self):
#         return str(self.value)

# class Float(Number):
#     value: float
#     type = FLOAT_TYPE

#     @sap_dunder
#     def add(self, other: Number, right: Bool) -> RuntimeVal:
#         if isinstance(other, (Int, Float)):
#             return Float(self.value + other.value)
#         return NOT_IMPLEMENTED()

#     @sap_dunder
#     def sub(self, other: Number, right: Bool) -> RuntimeVal:
#         if isinstance(other, (Int, Float)):
#             if right.value:
#                 return Float(other.value - self.value)
#             return Float(self.value - other.value)
#         return NOT_IMPLEMENTED()

#     @sap_dunder
#     def mul(self, other: Number, right: Bool) -> RuntimeVal:
#         if isinstance(other, (Int, Float)):
#             return Float(self.value * other.value)
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def truediv(self, other: Number, right: Bool) -> RuntimeVal:
#         if isinstance(other, (Int, Float)):
#             if right.value:
#                 return Float(other.value / self.value)
#             return Float(self.value / other.value)
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def floordiv(self, other: Number, right: Bool) -> RuntimeVal:
#         if isinstance(other, (Int, Float)):
#             if right.value:
#                 return Float(float(other.value // self.value))
#             return Float(float(self.value // other.value))
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def mod(self, other: Number, right: Bool) -> RuntimeVal:
#         if isinstance(other, (Int, Float)):
#             if right.value:
#                 return Float(float(other.value % self.value))
#             return Float(float(self.value % other.value))
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def exp(self, other: Number, right: Bool) -> RuntimeVal:
#         if isinstance(other, (Int, Float)):
#             if right.value:
#                 return Float(float(other.value ** self.value))
#             return Float(float(self.value ** other.value))
#         return NOT_IMPLEMENTED()

#     @sap_dunder
#     def sps(self, other: Number, right: Bool) -> RuntimeVal:
#         if isinstance(other, (Int, Float)):
#             if self.value < other.value:
#                 return Int(1 if right else -1)
#             if self.value > other.value:
#                 return Int(-1 if right else 1)
#             return Int(0)
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def float(self) -> Float:
#         return self
    
#     @sap_dunder
#     def int(self) -> Int:
#         return Int(int(self.value))

#     @sap_dunder
#     def str(self) -> Str:
#         return Str(str(self.value))

#     @sap_dunder
#     def repr(self) -> Str:
#         return Str(repr(self.value))


# class Str(RuntimeVal):
#     value: str
#     type = STR_TYPE

#     @typing.overload
#     def __init__(self, value: str): ...

#     @sap_dunder
#     def concat(self, other: Str, right: Bool) -> RuntimeVal:
#         if isinstance(other, Str):
#             if right.value:
#                 return Str(other.value + self.value)
#             return Str(self.value + other.value)
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def lmul(self, other: Int) -> RuntimeVal:
#         if isinstance(other, Int):
#             return Str(self.value * other.value)
#         return NOT_IMPLEMENTED()
    
#     @sap_dunder
#     def int(self) -> Int:
#         try:
#             return Int(int(self.value))
#         except ValueError:
#             raise errors.ValueError(f"Invalid literal for int() with base 10: '{self.value}'")

#     @sap_dunder
#     def float(self) -> Float:
#         try:
#             return Float(float(self.value))
#         except ValueError:
#             raise errors.ValueError(f"Invalid literal for float() with base 10: '{self.value}'")

#     @sap_dunder
#     def str(self) -> Str:
#         return Str(self.value)

#     @sap_dunder
#     def repr(self) -> Str:
#         return Str(repr(self.value))
    
#     def __str__(self):
#         return self.value
# class Bool(RuntimeVal):
#     value: bool
#     type = BOOL_TYPE

#     @typing.overload
#     def __init__(self, value: bool) -> None: ...

#     def __bool__(self): 
#         return self.value

#     @sap_dunder
#     def str(self) -> Str:
#         return Str(str(self.value).lower())

#     @sap_dunder
#     def bool(self) -> Bool:
#         return self

#     @sap_dunder
#     def int(self) -> Int:
#         return Int(1) if self.value else Int(0)
    
#     @sap_dunder
#     def float(self) -> Float:
#         return Float(1.0) if self.value else Float(0.0)

#     @sap_dunder
#     def repr(self) -> Str:
#         return Str(str(self.value).lower())

# class Null(RuntimeVal):
#     type = NULL_TYPE

#     @typing.overload
#     def __init__(self) -> None: ...

#     @sap_dunder
#     def bool(self) -> Bool: 
#         return False

#     @sap_dunder
#     def repr(self):
#         return "null"

# # I have to name it like this so that Python's NotImplemented is still usable
# class NOT_IMPLEMENTED(RuntimeVal):
#     type = NOT_IMPLEMENTED_TYPE

#     @typing.overload
#     def __init__(self) -> None: ...

#     @sap_dunder
#     def bool(self) -> Bool:
#         return False

#     @sap_dunder
#     def str(self):
#         return Str("NotImplemented")

#     @sap_dunder
#     def repr(self):
#         return Str("NotImplemented")

    

# class NativeCallable(RuntimeVal):
#     type = NATIVE_CALLABLE_TYPE

#     @typing.overload
#     def __init__(self, name, arguments, caller, return_hint): ...

#     name: str
#     arguments: tuple[FnArgument]
#     caller: typing.Callable[..., RuntimeVal]
#     return_hint: typing.Any