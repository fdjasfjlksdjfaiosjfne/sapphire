from typing import *

def _verify(hint: Any, obj: Any, mode: Literal["arg", "return"]) -> None:
    if mode not in {"arg", "return"}: 
        raise ValueError("Invalid mode inserted: must be 'arg' or 'return'.")
    phrase = "Argument" if mode == "args" else "Return value"
    origin = get_origin(hint)
    ## The match statement doesn't work :(
    
    if origin is NoReturn:
        if mode == "arg":
            raise TypeError("NoReturn should only be used for return statements of functions that never ends properly, not arguments.")
        raise TypeError("NoReturn should only be used for functions that never ends properly, like always throwing exceptions.")
    
    if origin is Union:
        if not isinstance(obj, get_args(hint)):
            raise ValueError(f"{phrase} should be one of these types: {[arg.__name__ for arg in get_args(hint)]}. Instead, it is {type(obj).__name__}")
        return
    
    if origin is Literal:
        if not any([obj == arg for arg in get_args(hint)]): # ! None of them matched
            raise ValueError(f"{phrase}")
        return
    
    return isinstance(obj, hint)
    # // if hint is NoReturn and mode == "arg":
    # //     raise ValueError(f"Invalid hint found on an argument: {hint}. This should be in return statements only.")
    # // if getattr(hint, '__origin__', None) is Union:
    # //     return hint.__args__
    # // if isinstance(hint, type):
    # //     return hint
    # // raise ValueError(f"Invalid hint: {hint}. Expected a type alias or NoReturn.")

F = TypeVar("F", bound = Callable[..., Any])

def enforce_types(fn: F) -> F:
    def wrapper(*args, **kwargs):
        hints = get_type_hints(fn)
        # ? Remove the return value from the dictionary to prevent errors
        return_type = 0
        if hints.get("return", 0) != 0:
            return_type = hints["return"]
            del hints["return"]
        
        # ? Check for the arguments
        for arg, hint in hints.items():
            if arg in kwargs:
                _verify(hint, arg, "arg")
            else:
                arg_value = args[list(hints.keys()).index(arg)]
                _verify(hint, arg_value, "arg")
        _verify(return_type, result := fn(*args, **kwargs), "return")
        return result
    return wrapper

@enforce_types
def greet(name: Literal["a", "b", "c"]) -> None:
    print(f"Hello, {name}!")

greet("d")