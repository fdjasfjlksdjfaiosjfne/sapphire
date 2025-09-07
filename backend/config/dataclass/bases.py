from __future__ import annotations

import abc
import dataclasses
import typing

if typing.TYPE_CHECKING:
    from backend.config.dataclass import RootConfigCls

from backend import errors

class ConfigDescriptorProtocol[T](typing.Protocol):
    @typing.overload
    def get(self) -> T: ...

    @typing.overload
    def get(self, *, return_unfilled: typing.Literal[False]) -> T: ...

    @typing.overload
    def get(self, *, return_unfilled: typing.Literal[True]) -> T | object: ...

    def is_default(self) -> bool: ...
    
    def is_explicit(self) -> bool: ...

_UNFILLED = object()
class ConfOptWrapper[T](ConfigDescriptorProtocol[T]):
    def __init__(self, value: T | object = _UNFILLED, default: T | object = _UNFILLED):
        self._v = value
        self._def = default
    
    @typing.overload
    def get(self) -> T: ...

    @typing.overload
    def get(self, *, return_unfilled: typing.Literal[False]) -> T: ...

    @typing.overload
    def get(self, *, return_unfilled: typing.Literal[True]) -> T | object: ...

    def get(self, *, return_unfilled: bool = False) -> T | object:
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

    def __bool__(self):
        return bool(self.get())

_MUTABLE_TYPES: dict[type, typing.Callable[[typing.Any], typing.Any]] = {list: tuple}

class CustomConfDatacls:
    """A custom wrapper for all config dataclasses.

    
    """
    _parent: typing.ClassVar = dataclasses.field(default = None, init = False)
    _root_cache = dataclasses.field(default = None, init = False)

    @abc.abstractmethod
    def validate_config(self) -> None:
        """Checks for any configuration errors that cannot be catched by the schema.
        """
        assert dataclasses.is_dataclass(self)
        for field in dataclasses.astuple(self):
            if isinstance(field, CustomConfDatacls):
                field.validate_config()
    
    @typing.final
    def get_root_config_cls(self):
        if self._parent is None:
            return typing.cast(RootConfigCls, self)
        if self._root_cache is None:
            c = self
            while c._parent is not None:
                if c._root_cache is not None:
                    c = c._root_cache
                    break
                c = c._parent
            self._root_cache = typing.cast(RootConfigCls, c)
        return self._root_cache

    def __post_init__(self) -> None:
        mutable_args: list[str] = getattr(self, "r4cr0q9Vmqd1d8Eb9Emh5pESG2Ts^*", [])
        # & Nothing ever happened...
        if hasattr(self, "r4cr0q9Vmqd1d8Eb9Emh5pESG2Ts^*"):
            object.__delattr__(self, "r4cr0q9Vmqd1d8Eb9Emh5pESG2Ts^*")

        for arg_name in mutable_args:
            arg = getattr(self, arg_name)
            if isinstance(arg, list):
                arg = tuple(arg)
            setattr(self, arg_name, arg)
        

    def __init__(self, **kwargs) -> None:
        if not dataclasses.is_dataclass(self):
            raise errors.InternalError(
                "Any subclasses of CustomDataclass must be a dataclass"
            )

        def assign_default(field):
            default = field.default
            if default is not dataclasses.MISSING:
                if dataclasses.is_dataclass(default):
                    return  # skip dataclass defaults
                if not isinstance(default, ConfOptWrapper):
                    default = ConfOptWrapper(_UNFILLED, default)
                object.__setattr__(self, field.name, default)
                return

            if field.default_factory is not dataclasses.MISSING:
                val = field.default_factory()
                if dataclasses.is_dataclass(val):
                    return  # skip dataclass defaults
                if not isinstance(val, ConfOptWrapper):
                    val = ConfOptWrapper(_UNFILLED, val)
                object.__setattr__(self, field.name, val)
                return

            raise errors.InternalError(
                f"Missing attribute without any default value: {field.name} in {type(self).__name__}"
            )

        def assign_value(field, value):
            if isinstance(value, CustomConfDatacls):
                object.__setattr__(value, "parent", self)
                object.__setattr__(self, field.name, value)
            else:
                object.__setattr__(self, field.name, ConfOptWrapper(value, field.default))

        for field in dataclasses.fields(self):
            if not field.init:
                continue
            typ = field.type
            if typing.get_origin(typ) is typing.ClassVar:
                continue
            if typ in _MUTABLE_TYPES:
                if not hasattr(self, "r4cr0q9Vmqd1d8Eb9Emh5pESG2Ts^*"):
                    setattr(self, "r4cr0q9Vmqd1d8Eb9Emh5pESG2Ts^*", [])
                getattr(self, "r4cr0q9Vmqd1d8Eb9Emh5pESG2Ts^*").append(field.name)
            if field.name not in kwargs:
                assign_default(field)
            else:
                assign_value(field, kwargs.pop(field.name))

        if kwargs:
            raise errors.InternalError(
                f"{type(self).__name__}.__init__() recieve redundant keyword arguments ({','.join(kwargs.keys())})"
            )
        self.validate_config()
