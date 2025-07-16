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

def dunder_dict(fn) -> dict:
    """Collect all methods from a function and return them as a dict.

    Well...sort of.

    The functions that is attached with this decorator is expected to return its local scope using `locals()`.

    So this, quite literally, just replace the decorated function with its return value.
    """
    return fn()

class RuntimeVal(metaclass = RuntimeValMeta):
    """Base class for all runtime values in the Sapphire language."""
    props: dict[str, typing.Any]

class Object(RuntimeVal):
    @dunder_dict
    def props():
        return locals()