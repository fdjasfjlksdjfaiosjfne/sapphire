import dataclasses
import typing

from sympy import continued_fraction

from backend import errors

class ConfigDescriptorProtocol[T](typing.Protocol):
    @typing.overload
    def get_value(self) -> T: ...

    @typing.overload
    def get_value(self, *, return_unfilled: typing.Literal[False]) -> T: ...

    @typing.overload
    def get_value(self, *, return_unfilled: typing.Literal[True]) -> T | object: ...

    def is_default(self) -> bool: ...
    
    def is_explicit(self) -> bool: ...

_UNFILLED = object()
class ConfigDescriptor[T](ConfigDescriptorProtocol[T]):
    def __init__(self, value: T | object, default: T): 
        self.__v = value
        self.__def = default
    
    def __getattr__(self, name: str):
        if hasattr(self.__v, name):
            return getattr(self.__v, name)
        raise AttributeError(f"No attribute name: {name}")
    
    @typing.overload
    def get_value(self) -> T: ...

    @typing.overload
    def get_value(self, *, return_unfilled: typing.Literal[False]) -> T: ...

    @typing.overload
    def get_value(self, *, return_unfilled: typing.Literal[True]) -> T | object: ...
    

    def get_value(self, *, return_unfilled: bool = False) -> T | object:
        """Return the pure value store in the descriptor.

        The keyword-only `return_unfilled` argument determines whether 
        the method will return the default value if the value is the 
        `_UNFILLED` sentinel object.
        """
        if self.__v is _UNFILLED and not return_unfilled:
            return self.__def
        return self.__v
    
    def is_default(self):
        return self.__v is _UNFILLED
    
    def is_explicit(self):
        return self.__v is not _UNFILLED

class CustomDataclass:
    def __init__(self, **kwargs) -> None:
        if not dataclasses.is_dataclass(self):
            raise errors.InternalError(
                "Any subclasses of CustomDataclass must be a dataclass"
            )
        for field in dataclasses.fields(self):
            if field.name not in kwargs:
                default = field.default
                if default is not dataclasses.MISSING:
                    if dataclasses.is_dataclass(field.default):
                        continue
                    if not isinstance(default, ConfigDescriptor):
                        default = ConfigDescriptor(_UNFILLED, default)
                    object.__setattr__(self, field.name, default)
                
                elif field.default_factory is not dataclasses.MISSING:
                    val = field.default_factory()
                    if dataclasses.is_dataclass(val):
                        continue
                    if not isinstance(field.default, ConfigDescriptor):
                        default = ConfigDescriptor(_UNFILLED, val)
                    object.__setattr__(self, field.name, default)
                
                else:
                    raise errors.InternalError(
                        f"Missing attribute without any default value: {field.name} in {type(self).__name__}"
                    )
            else:
                object.__setattr__(self, field.name, ConfigDescriptor(kwargs.pop(field.name), field.default))
        if kwargs:
            raise AttributeError(
                f"{type(self).__name__}.__init__() recieve redundant keyword arguments ({",".join(kwargs.keys())})"
            )