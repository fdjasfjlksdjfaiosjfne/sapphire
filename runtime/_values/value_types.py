from __future__ import annotations

import abc
import copy
import itertools
import typing

from backend import errors
from parser import nodes
from runtime import env

class RuntimeValue:
    """Base class for all runtime values"""
    type: Type | None
    attributes: dict[str, typing.Any | typing.Callable]
    def __init__(self):
        for base in reversed(type(self).mro()):
            for k, v in getattr(base, "attributes", {}).items():
                self.attributes[k] = v
        

    def get_attribute(self, name, default) -> RuntimeValue: 
        """Get attributes from the runtime value."""
        # $ Check instance dictionary
        if hasattr(self, "attributes") and name in self.attributes:
            
            attr = self.attributes[name]
            assert isinstance(attr, RuntimeValue)
            if self.is_method(attr):
                return attr.bind(self)
            return attr
        
        # $ Scroll through the MRO
        if self.type is not None:
            for type_in_mro in self.type.mro:
                if name in type_in_mro.attributes:
                    attr = type_in_mro.attributes[name]
                    assert isinstance(attr, RuntimeValue)
                    # Handle method binding for class methods too
                    if self.is_method(attr):
                        return attr.bind(self)
                    return attr
        raise errors.InProgress
    
    def set_attribute(self, name, value):
        raise errors.InProgress
        # Handle attribute setting
    
    @staticmethod
    def is_method(obj) -> typing.TypeGuard[FunctionValue]:
        return isinstance(obj, FunctionValue)

    def call_method(self, method_name, args = [], kwargs = {}):
        raise errors.InProgress
    

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
        """Compute Method Resolution Order using C3 linearization"""
        if not self.bases:
            return [self]
        
        base_mros = [base.mro for base in self.bases]
        mro = [self] + self._c3_merge(base_mros + list(self.bases))
        return mro
    
    def _c3_merge(self, sequences):
        """C3 merge algorithm"""
        result = []
        while True:
            # Remove empty sequences
            sequences = [seq for seq in sequences if seq]
            if not sequences:
                break

            # ? Find a good candidate
            # $ It should appears first in some sequence and
            # $ in the tail of any sequence
            candidate = None
            for seq in sequences:
                head = seq[0]
                if not any(head in seq[1:] for seq in sequences):
                    candidate = head
                    break
            
            if candidate is None:
                raise errors.TypeError("Inconsistent MRO - cannot create a valid linearization")
            
            result.append(candidate)
            # Remove candidate from all sequences
            for seq in sequences:
                if seq and seq[0] == candidate:
                    seq.pop(0)
        return result

    def create_instance(self):
        instance = Instance(self)
        # Call __init__ if it exists
        return instance

class Instance(RuntimeValue):
    """Instances of user-defined classes"""
    def __init__(self, type_obj):
        super().__init__()
        self.type_obj = type_obj

class NumberValue(RuntimeValue): 
    value: int | float

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
            raise errors.TypeError(f"__bool__ returns non-bool value ({value!r})")
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
        RuntimeValue.__init__(self)
        self.value = bool(value)

class StringValue(RuntimeValue):
    def __new__(cls, value):
        if isinstance(value, RuntimeValue):
            val = value.call_method("__str__")
            if isinstance(val, StrValue):
                return val
            raise errors.TypeError(f"__str__ returns non-string value ({value!r})")
        return super().__new__(cls)
    def __init__(self, value):
        if hasattr(self, 'value'): # Already initialized (from cache)
            return
        super().__init__()
        self.value = str(value)

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

class ListValue(RuntimeValue):
    def __init__(self, value = None):
        self.value = list(value or [])

class TupleValue(RuntimeValue):
    def __init__(self, value = None):
        self.value = list(value or [])

class SetValue(RuntimeValue):
    def __init__(self, value = None):
        self.value = set(value or [])

class DictValue(RuntimeValue):
    def __init__(self, value = None):
        self.value = dict(value or {})

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
        self.pos_only_args = posonlys or []
        self.hybrid_args = arguments or []
        self.kw_only_args = keyonlys or []
        self.variadic_pos = variadic_pos
        self.variadic_key = variadic_key
        for arg_name in ("positional_only_arguments", "arguments", "keyword_only_arguments"):
            if getattr(self, arg_name) is None:
                setattr(self, arg_name, [])

class FunctionValue(RuntimeValue):
    args: FnArguments
    return_hint: None
    @abc.abstractmethod
    def bind(self, instance) -> FunctionValue: ...
    @abc.abstractmethod
    def call(self, parent_env: env.Env, args: list, kwargs: dict) -> RuntimeValue: ...

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
        if args.pos_only_args:
            args.pos_only_args = args.pos_only_args[1:]
        elif args.hybrid_args:
            args.hybrid_args = args.hybrid_args[1:]
        else:
            raise errors.ValueError("Cannot bind 'self' into method")
        return NativeFunctionValue(
            self.name,
            args,
            lambda *args, **kwargs: self.caller(instance, args, kwargs),
            self.return_hint
        )
    def call(self, parent_env, args: list, kwargs: dict) -> RuntimeValue:
        if self.needs_env:
            return self.caller(args, kwargs, env = parent_env)
        else:
            return self.caller(args, kwargs)

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
        if args.pos_only_args:
            args.pos_only_args = args.pos_only_args[1:]
        elif args.hybrid_args:
            args.hybrid_args = args.hybrid_args[1:]
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
    
    def call(self, parent_env: env.Env, args: list[RuntimeValue], kwargs: dict[str, RuntimeValue]) -> RuntimeValue:
        from runtime.interpreter import evaluate
        call_env = env.Env(parent_env)
        if self.args.variadic_pos is not None:
            call_env.assign(self.args.variadic_pos.name, TupleValue())
        if self.args.variadic_key is not None:
            call_env.assign(self.args.variadic_key.name, DictValue())

        # $ Applying arguments
        # & Don't ask me it's this long

        def inserted_args_generator():
            yield from args
        
        def expected_pos_only_args_generator():
            yield from self.args.pos_only_args
        
        def expected_hybrid_args_generator():
            yield from self.args.hybrid_args

        iag = inserted_args_generator()
        epag = expected_pos_only_args_generator()
        ehag = expected_hybrid_args_generator()
        occupied_hybrid_args = []
        for called, expected in zip(iag, epag):
            call_env.assign(expected.name, called)
        
        # ? Checking whether there's any missing or there's too much arguments
        number_of_inserted_args = len(args)
        number_of_expected_posonly_args = len(self.args.pos_only_args)

        if number_of_inserted_args < number_of_expected_posonly_args:
            if (first_ := next(epag)).default is None:
                raise errors.ArgumentError(
                    f"Function {self.name} expecting {number_of_expected_posonly_args} "
                    f"positional arguments, got {number_of_inserted_args}"
                )
            
            # $ All argument from this point should have default arguments
            for missing_arg in itertools.chain([first_], epag):
                if missing_arg.default is None:
                    raise errors.InternalError(
                        "It seems that an argument that does not have a default "
                        f"value ('{missing_arg.name}') appears after an argument "
                        "with one. This should not happened."
                    )
                call_env.assign(missing_arg.name, missing_arg.default)
        if number_of_expected_posonly_args > number_of_inserted_args:
            # $ Alright, hybrid arguments time
            for inserted, expected in zip(iag, ehag):
                occupied_hybrid_args.append(expected.name)
                call_env.assign(expected.name, inserted)
            number_of_inserted_args = number_of_inserted_args - number_of_expected_posonly_args
            number_of_expected_hybrid_args = len(self.args.hybrid_args)
            if number_of_inserted_args < number_of_expected_hybrid_args:
                if (first_ := next(ehag)).default is None:
                    raise errors.ArgumentError(
                        f"Function {self.name} expecting {number_of_expected_posonly_args} "
                        f"positional arguments, got {number_of_inserted_args}"
                    )
                
                # $ All argument from this point should have default arguments
                for missing_arg in itertools.chain([first_], ehag):
                    if missing_arg.default is None:
                        raise errors.InternalError(
                            "It seems that an argument that does not have a default "
                            f"value ('{missing_arg.name}') appears after an argument "
                            "with one. This should not happened."
                        )
                    call_env.assign(missing_arg.name, missing_arg.default)
            elif number_of_inserted_args > number_of_expected_hybrid_args:
                if self.args.variadic_pos is None:
                    raise errors.ArgumentError(
                        f"Expecting {number_of_expected_posonly_args + number_of_expected_hybrid_args}, "
                        f"got {number_of_inserted_args + number_of_expected_posonly_args}"
                    )
                call_env.assign(self.args.variadic_pos.name, TupleValue(iag))
        
        # $ Filling in keyword arguments
        keyword_args = list(ehag) + self.args.kw_only_args
        keyword_arg_names = [i.name for i in keyword_args]

        for k in list(kwargs.keys()): # Make sure it does NOT change...
            if k in keyword_arg_names:
                call_env.assign(k, kwargs.pop(k))
                index = keyword_arg_names.index(k)
                keyword_arg_names.pop(index)
                keyword_args.pop(index)
            if k in occupied_hybrid_args:
                raise errors.InternalError(
                    f"Argument '{k}', which is attempted to being filled "
                    "using keywords, has already been filled positionally "
                    f"(at position {occupied_hybrid_args.index(k)}) "
                )
        if kwargs:
            if self.args.variadic_key is None:
                raise errors.AttributeError(
                    "Redundant keyword arguments are given "
                    f"({", ".join(kwargs.keys())})"
                )
            call_env.assign(self.args.variadic_key.name, DictValue(kwargs))
        
        missing_args = []
        for i in keyword_args:
            if i.default is None:
                missing_args.append(i.name)
            else:
                call_env.assign(i.name, i.default)
        
        if len(missing_args) == 1:
            raise errors.AttributeError(
                f"A keyword argument ({missing_args[0]}) is not filled."
            )
        if missing_args:
            raise errors.AttributeError(
                f"Missing keyword arguments ({", ".join(missing_args)})"
            )

        # Run the function
        try:
            evaluate(self.code_block, call_env)
        except errors.ReturnValue as e:
            return e.args[0]
        return NULL

class BoundCustomFunction(CustomFunctionValue):
    def __init__(self, name, args, code_block, return_hint, bound_instance, original_func):
        super().__init__(name, args, code_block, return_hint)
        self.bound_instance = bound_instance
        self.original_func = original_func
    
    def call(self, parent_env, args, kwargs):
        return self.original_func.call(parent_env, [self.bound_instance] + args, kwargs)

# ? Global constant singletons
TRUE = BoolValue(True)
FALSE = BoolValue(False)
NULL = NullValue()
NOT_IMPLEMENTED = NotImplementedValue()