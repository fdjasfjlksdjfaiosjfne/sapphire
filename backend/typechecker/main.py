from typing import *
from .resources import Verify

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
        for arg_name, hint in hints.items():
            if arg_name in kwargs:
                Verify.verify_hint(hint, kwargs[arg_name], arg_name)
            else:
                arg_value = args[list(hints.keys()).index(arg_name)]
                Verify.verify_hint(hint, arg_value, arg_name)
        Verify.verify_hint(return_type, result := fn(*args, **kwargs), "return")
        return result
    return wrapper

@enforce_types
def greet(name: Literal["a", "b", "c"]) -> None:
    print(f"Hello, {name}!")

greet("d")