from calendar import c
import dataclasses
import typing

from backend import errors

_UNFILLED = object()

class ConfigDescriptor[T]:
    def __init__(self, value: T, default: T = _UNFILLED): 
        self._v = value
        if default is _UNFILLED:
            self._def = self._v
    
    def __get__(self, obj, owner = None):
        if obj is None:
            return self
        return self.get_value()
    
    def get_value(self, *, return_unfilled: bool = False):
        """Return the pure value store in the descriptor.

        The keyword-only `return_unfilled` argument determines whether 
        the method will return the default value if the value is the 
        `_UNFILLED` sentinel object.
        """
        if self._v is _UNFILLED and not return_unfilled:
            return self._def
        return self._v
    
    def is_default(self):
        return self._v is _UNFILLED
    
    def is_explicit(self):
        return self._v is not _UNFILLED

    def __set__(self, obj, value): # & Extra frozen measure 👍
        raise errors.InternalError(
            "Any of the values in the config class are not allowed to be modified."
        )
    
    def __del__(self, obj, owner = None):
        raise errors.InternalError(
            "Any of the values in the config class are not allowed to be deleted."
        )

    def __delete__(self, obj, owner = None):
        raise errors.InternalError(
            "Any of the values in the config class are not allowed to be deleted."
        )

class CustomDataclass:
    def __init__(self, **kwargs) -> None:
        if not dataclasses.is_dataclass(self):
            raise errors.InternalError(
                "Any subclasses of CustomDataclass must be a dataclass"
            )
        for field in dataclasses.fields(self):
            if field.name not in kwargs:
                if field.default is not dataclasses.MISSING:
                    object.__setattr__(self, field.name, ConfigDescriptor(_UNFILLED, field.default))
                elif field.default_factory is not dataclasses.MISSING:
                    object.__setattr__(self, field.name, ConfigDescriptor(_UNFILLED, field.default_factory()))
            else:
                object.__setattr__(self, field.name, ConfigDescriptor(kwargs.pop(field.name)))
        if kwargs:
            raise AttributeError(
                f"{type(self).__name__}.__init__() recieve redundant keyword arguments ({",".join(kwargs.keys())})"
            )