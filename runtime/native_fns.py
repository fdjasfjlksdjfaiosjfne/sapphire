"""
    This module contains the native functions that are built into the language.
    They are functions that are not defined using the language, but can be access using it.
"""

# from typing import Dict, Callable, Any

# class NativeFunctionRegistry:
#     def __init__(self):
#         self._functions: Dict[str, Callable] = {}
    
#     def register(self, name: str, fn: Callable):
#         self._functions[name] = fn
    
#     def get(self, name: str) -> Callable:
#         return self._functions.get(name)

# # Global registry instance
# native_registry = NativeFunctionRegistry()

# def native_function(name: str):
#     def decorator(fn: Callable):
#         native_registry.register(name, fn)
#         return fn
#     return decorator

# @native_function("print")
# def native_print(*values, sep, end, file, flush):
#     print(*values, sep, end, file, flush)

# @native_function("len")
# def native_len(obj):
#     pass

# @native_function("type")
# def native_type(obj):
#     return type(obj).__name__

