from __future__ import annotations

import copy
import typing

from backend import errors
from parser import nodes
from runtime import env

__all__ = [
    "RuntimeValue",
    "Type",
    "IntValue",
    "FloatValue",
    "BoolValue",
    "NullValue",
    "NotImplementedValue",
    "TRUE",
    "FALSE",
    "NULL",
    "NOT_IMPLEMENTED",
    "FunctionValue",
    "CustomFunctionValue",
    "NativeFunctionValue",
    "BoundCustomFunction",
    "FnArguments",
    "FnArgument"
]

class RuntimeValue:
    """Base class for all runtime values"""
    type: Type | None
    attributes: dict[str, typing.Any | typing.Callable]
    def __init__(self):
        for base in reversed(type(self).mro()):
            for k, v in getattr(base, "attributes", {}).items():
                self.attributes[k] = v
        

    def get_attribute(self, name): 
        """Get attributes from the runtime value."""
        # $ Check instance dictionary
        if hasattr(self, "attributes") and name in self.attributes:
            attr = self.attributes[name]
            if self.is_method(attr):
                return self.bind_method(attr)
            return attr
        
        # $ Scroll through the 
        if self.type is not None:
            for type_in_mro in self.type.mro:
                if name in type_in_mro.attributes:
                    attr = type_in_mro.attributes[name]
                    # Handle method binding for class methods too
                    if self.is_method(attr):
                        return self.bind_method(attr)
                    return attr
    
    def set_attribute(self, name, value):
        raise errors.InternalError("TBA")
        # Handle attribute setting
        
    def is_method(self, obj) -> bool:
        raise errors.InternalError("TBA")

    def call_method(self, method_name, args = [], kwargs = {}):
        raise errors.InternalError("TBA")
    
    def bind_method(self, attr):
        pass

class Type(RuntimeValue):
    """Represents classes/types (like Python's type)"""
    def __init__(self, name, bases = None, methods = None):
        super().__init__()
        self.name = name
        self.bases = bases or []
        self.methods = methods or {}
        self.mro = self.compute_mro() # Method Resolution Order
        self.type_obj = self  # Types are instances of themselves (or a metaclass later)
    
    def compute_mro(self):
        return []

    def create_instance(self):
        instance = Instance(self)
        # Call __init__ if it exists
        return instance

class Instance(RuntimeValue):
    """Instances of user-defined classes"""
    def __init__(self, type_obj):
        super().__init__()
        self.type_obj = type_obj

class IntValue(RuntimeValue):
    _cache = {}
    def __new__(cls, value):
        if isinstance(value, RuntimeValue):
            val = value.call_method("__int__")
            if isinstance(val, IntValue):
                return val
            raise errors.TypeError(f"__int__ returns non-int value ({value!r})")
        try:
            py_value = int(value) # type: ignore
        except ValueError:
            raise errors.InternalError(f"IntValue recieve invalid value ({value!r})")
        if -5 <= py_value <= 256:
            if py_value not in cls._cache:
                instance = super().__new__(cls)
                instance.__init__(py_value)
                cls._cache[py_value] = instance
            return cls._cache[py_value]
        else:
            # Large numbers get fresh instances
            return super().__new__(cls)
    def __init__(self, value):
        if hasattr(self, 'value'): # Already initialized (from cache)
            return
        super().__init__()
        self.value = int(value)

class FloatValue(RuntimeValue):
    _cache = {}
    def __new__(cls, value):
        if isinstance(value, RuntimeValue):
            val = value.call_method("__float__")
            if isinstance(val, FloatValue):
                return val
            raise errors.TypeError(f"__float__ returns non-int value ({value!r})")
        try:
            py_value = float(value) # type: ignore
        except ValueError:
            raise errors.InternalError(f"FloatValue recieve invalid value ({value!r})")
        if -5 <= py_value <= 256:
            if py_value not in cls._cache:
                instance = super().__new__(cls)
                instance.__init__(py_value)
                cls._cache[py_value] = instance
            return cls._cache[py_value]
        else:
            # Large numbers get fresh instances
            return super().__new__(cls)
    def __init__(self, value):
        if hasattr(self, 'value'): # Already initialized (from cache)
            return
        super().__init__()
        self.value = float(value)

class BoolValue(IntValue):
    _cache = {}
    def __new__(cls, value):
        if isinstance(value, RuntimeValue):
            val = value.call_method("__bool__")
            if isinstance(val, BoolValue):
                return val
            raise errors.TypeError(f"__bool__ returns non-int value ({value!r})")
        try:
            py_value = bool(value) # type: ignore
        except ValueError:
            raise errors.InternalError(f"BoolValue recieve invalid value ({value!r})")
        if py_value not in cls._cache:
            instance = super().__new__(cls, int(py_value))
            instance.__init__(py_value)
            cls._cache[py_value] = instance
        return cls._cache[py_value]
    def __init__(self, value):
        if hasattr(self, 'value'): # Already initialized (from cache)
            return
        super().__init__(value)
        self.value = bool(value)

class NullValue(RuntimeValue):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

class NotImplementedValue(RuntimeValue):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

class FnArgument(typing.NamedTuple):
    name: str
    default: RuntimeValue | None = None
    hint: typing.Any = None # todo add type hint support...

class FnArguments:
    def __init__(self,
                 posonlys: list[FnArgument] | None = None,
                 arguments: list[FnArgument] | None = None,
                 keyonlys: list[FnArgument] | None = None,
                 variadic_pos: FnArgument | None = None,
                 variadic_key: FnArgument | None = None
                ):
        self.positional_only_arguments = typing.cast(list[FnArgument], posonlys)
        self.arguments = typing.cast(list[FnArgument], arguments)
        self.keyword_only_arguments = typing.cast(list[FnArgument], keyonlys)
        self.variadic_pos = variadic_pos
        self.variadic_key = variadic_key
        for arg_name in ("positional_only_arguments", "arguments", "keyword_only_arguments"):
            if getattr(self, arg_name) is None:
                setattr(self, arg_name, [])

class FunctionValue(RuntimeValue):
    args: FnArguments
    return_hint: None

class NativeFunctionValue(FunctionValue):
    def __init__(self, 
                 name: str,
                 arguments: FnArguments, 
                 caller: typing.Callable, 
                 return_hint = None, 
                 needs_env: bool = False):
        self.name = name
        self.args = arguments
        self.caller = caller
        self.return_hint = return_hint
        self.needs_env = needs_env
    
    def bind(self, instance):
        args = copy.copy(self.args)
        if args.positional_only_arguments:
            args.positional_only_arguments = args.positional_only_arguments[1:]
        elif args.arguments:
            args.arguments = args.arguments[1:]
        else:
            raise errors.ValueError("Cannot bind 'self' into method")
        return NativeFunctionValue(
            self.name,
            args,
            lambda *args, **kwargs: self.caller(instance, args, kwargs),
            self.return_hint
        )
    def call(self, parent_env: env.Env, args: list, kwargs: dict):
        if self.needs_env:
            return self.caller(args, kwargs, __env__ = env.Env(parent_env)) # Pass env to natives that need it
        else:
            return self.caller(args, kwargs)  # Most natives don't need env

class CustomFunctionValue(FunctionValue):
    def __init__(self, 
                 name: str, 
                 arguments: FnArguments, 
                 code_block: nodes.CodeBlockNode, 
                 return_hint = None
                ):
        self.name = name
        self.args = arguments
        self.code_block = code_block
        self.return_hint = return_hint
    
    def bind(self, instance):
        args = copy.copy(self.args)
        if args.positional_only_arguments:
            args.positional_only_arguments = args.positional_only_arguments[1:]
        elif args.arguments:
            args.arguments = args.arguments[1:]
        else:
            raise errors.ValueError("Cannot bind 'self' into method")
        bound_fn = BoundCustomFunction(
            name = self.name, 
            args = args,
            code_block = self.code_block,
            return_hint = self.return_hint,
            bound_instance = instance,
            original_func = self
        )
        return bound_fn
    
    def call(self, parent_env: env.Env, args: list, kwargs: dict):
        call_env = env.Env(parent_env)

class BoundCustomFunction(CustomFunctionValue):
    def __init__(self, name, args, code_block, return_hint, bound_instance, original_func):
        super().__init__(name, args, code_block, return_hint)
        self.bound_instance = bound_instance
        self.original_func = original_func
    
    def call(self, parent_env, args, kwargs):
        return self.original_func.call(parent_env, [self.bound_instance] + args, kwargs)

# ? Global constants
TRUE = BoolValue(True)
FALSE = BoolValue(False)
NULL = NullValue()
NOT_IMPLEMENTED = NotImplementedValue()