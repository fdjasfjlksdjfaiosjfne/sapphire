"""
    This module contains the native functions that are built into the language.
    They are functions that are not defined using the language, but can be access using it.
"""

import runtime.values as Values
import builtins

# abs() aiter() all() anext() any() ascii() bin() bool() callable()
# chr() classmethod() compile() complex() delattr() dict() dir()
# divmod() filter() float() format() frozenset() getattr() globals()
# hasattr() hash() help() hex() input() int() isinstance() issubclass()
# iter() len() list() locals() map() max() memoryview() min() next()
# object() oct() open() ord() pow() print() property() range() repr()
# reversed() round() set() setattr() slice() sorted() staticmethod()
# str() sum() super() tuple() type() vars() zip() __import__()

def print(*args, sep, file, end):
    builtins.print(
        *(Values.StringValue(obj) for obj in args), 
        sep = sep,
        file = file,
        end = end
    )
    return Values.NullValue()

# def s_len(obj: Values.RuntimeVal, /):
#     __len__ = obj.__sap_dunder_map__.get("__len__", None)
#     if callable(__len__):
#         return __len__()

# def s_type(obj: Values.RuntimeVal, /):
#     pass

# def s_bool(obj: Values.RuntimeVal, /):
#     __bool__ = obj.__sap_dunder_map__.get("__bool__", None)
#     if callable(__bool__):
#         return __bool__()

# def s_int(obj: Values.RuntimeVal, /):
#     __int__ = obj.__sap_dunder_map__.get("__int__", None)
#     if callable(__int__):
#         return __int__()

# def s_repr(obj: Values.RuntimeVal, /):
#     __repr__ = obj.__sap_dunder_map__.get("__repr__", None)
#     if callable(__repr__):
#         return __repr__()

# def s_str(obj: Values.RuntimeVal, /):
#     __str__ = obj.__sap_dunder_map__.get("__repr__", None)
#     if callable(__str__):
#         return __str__()