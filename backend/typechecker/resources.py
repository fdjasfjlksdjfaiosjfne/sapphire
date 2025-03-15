from typing import *
from inspect import *
from types import *

class Verify:
    @classmethod
    @overload
    def _(cls, hint, value: Any, arg_name: str, *, return_bool: Literal[True] = True) -> bool:...

    @classmethod
    @overload
    def _(cls, hint, value: Any, *, return_bool: Literal[True] = True) -> bool:...
    
    @classmethod
    @overload
    def _(cls, hint, *, return_bool: Literal[True] = True) -> bool:...

    @classmethod
    @overload
    def _(cls, hint, value: Any, arg_name: str, *, return_bool: Literal[False] = False) -> Union[NoReturn, None]:...

    @classmethod
    def _(cls, hint, value: Any = None, arg_name: str = None, return_bool: bool = False) -> Union[NoReturn, None, bool]:
        if value == None:
            value = cls.value
        if arg_name == None:
            arg_name = cls.arg_name
        cls.hint = hint
        cls.value = value
        cls.arg_name = arg_name
        cls.return_bool = return_bool
        origin = get_origin(hint)
        
        if not isinstance(hint, type):
            return cls.throw(f"{hint} is not a valid type hint.")
        
        if origin is Any:
            return
        elif origin is Union:
            return cls.Union()
        elif origin is Optional:
            return cls.Optional()
        elif origin is Callable:
            return cls.Callable()
        elif origin is List:
            return cls.verify_list_hint()
        elif origin is Tuple:
            return cls.verify_tuple_hint()
        elif origin is Set:
            return cls.verify_set_hint()
        elif origin is Dict:
            return cls.verify_dict_hint()
        else:
            if not isinstance(value, hint):
                return cls.throw(f"Expecting {hint} in '{arg_name}', recieve {value} of {type(value)} instead.")
            cls.dispose()
    
    @classmethod
    def dispose(cls):
        r_value = None
        if cls.return_bool:
            r_value = True
        
        del cls.hint
        del cls.arg_name
        del cls.value
        del cls.return_bool
        
        return r_value
    
    @classmethod
    def throw(cls, name: str):
        if cls.return_bool:
            return False
        raise ValueError(name)
    
    @classmethod
    def Union(cls):
        args = get_args(cls.hint)
        if not any( [cls._(args, return_bool = True) for arg in args] ):
            return cls.throw(f"Expecting any of these types in '{cls.arg_name}': {cls.args}, recieve {cls.value} of {type(cls.value)} instead.")
        cls.dispose()

    @classmethod
    def Optional(cls):
        if not (isinstance(cls.value, None) or cls._(get_args(cls.hint), return_bool = True)):
            return cls.throw(f"Expecting either {cls.hint} or None in '{cls.arg_name}', recieve {cls.value} of {type(cls.value)} instead.")
        cls.dispose()
    
    @classmethod
    def Callable(cls):
        args = get_args(cls.hint)
        arg_hints = args[0]; return_hint = args[1]
        
        if not (isinstance(cls.value, (function, BuiltinFunctionType, BuiltinMethodType) or hasattr(cls.value, "__call__"))):
            return cls.throw(f"")
        
        type_hints = get_type_hints(cls.value)
        return_hin = type_hints.pop("return")
        raise Exception("unfinished")
    
    @classmethod
    def verify_list_hint(cls):
        arg = get_args(cls.hint)
        if not isinstance(cls.value, list):
            return cls.throw(f"Expecting a list in '{cls.arg_name}', recieve {cls.value} of {type(cls.value)}")
        if not all([cls._(arg, element, return_bool = True) for element in cls.value]):
            return cls.throw(f"")
        cls.dispose()

    @classmethod
    def verify_tuple_hint(cls):
        if not isinstance(cls.value, tuple):
            return cls.throw(f"Expecting a tuple in '{cls.arg_name}', recieve {cls.value} of {type(cls.value)} instead.")
        args = get_args(cls.hint)
        if args[1] is EllipsisType:
            if not any( [cls._(args[0], element, return_bool = True) for element in cls.value] ):
                return cls.throw(f"")
        else:
            if len(args) != len(cls.value):
                return cls.throw(f"")
            if not all( [cls._(args[index], element, return_bool = True) for index, element in enumerate(cls.value)] ):
                return cls.throw(f"")
        cls.dispose()
    
    @classmethod
    def verify_set_hint(cls):
        arg = get_args(cls.hint)
        if not isinstance(cls.value, set):
            return cls.throw(f"Expecting a set in '{cls.arg_name}', recieve {cls.value} of {type(cls.value)} instead.")
        if not all([cls._(arg, element, return_bool = True) for element in cls.value]):
            return cls.throw(f"")
        cls.dispose()
    
    @classmethod
    def verify_dict_hint(cls):
        args = get_args(cls.hint)
        key_hint = args[0]; value_hint = args[1]
        if not isinstance(cls.value, dict):
            return cls.throw(f"Expecting a dictionary in '{cls.arg_name}', recieve {cls.value} of {type(cls.value)} instead.")
        if not all([cls._(key_hint, key, return_bool = True) and cls._(value_hint, value, return_bool = True) for key, value in cls.value.items()]):
            return cls.throw(f"")
        cls.dispose()