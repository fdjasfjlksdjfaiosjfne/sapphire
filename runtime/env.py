from __future__ import annotations
import typing
from runtime.values import values
from backend import errors
class Env:
    def __init__(self, parent: typing.Optional[Env] = None):
        self.parent = parent
        self.variables: dict[str, values.RuntimeValue | None] = {}
        self.constants: list[str] = []

    def declare(self, name: str, value: values.RuntimeValue | None = None, const: bool = False) -> None:
        if name in self.variables:
            raise errors.VariableError(f"Variable '{name}' is already declared")
        if const and value is None:
            raise errors.SyntaxError("A constant declaration must include a value")
        self.variables.setdefault(name, value)
        if const:
            self.constants.append(name)
        
    def is_constant(self, name: str):
        return name in self.constants
    
    def assign(self, name: str, value: values.RuntimeValue) -> None:
        if name in self.variables:
            if self.is_constant(name):
                raise errors.VariableError("Cannot change a constant value")
        self.variables[name] = value
    
    def get(self, name: str) -> values.RuntimeValue:
        env = self.resolve(name)
        var = env.variables.get(name)
        if var is None:
            raise errors.VariableError(f"Variable '{name}', although declared, has not been assigned")
        return var

    def resolve(self, name: str) -> Env | typing.NoReturn:
        if name in self.variables.keys():
            return self
        if self.parent == None:
            raise errors.VariableError(f"Variable '{name}' is not assigned")
        return self.parent.resolve(name)
    
    def __getitem__(self, key: str) -> values.RuntimeValue | None:
        return self.variables[key]
    
    def __setitem__(self, key: str, value: values.RuntimeValue) -> None:
        if self.is_constant(key):
            raise errors.VariableError("Cannot change a constant value")
        self.variables.setdefault(key, value)
    
    def __contains__(self, ident: str) -> bool:
        return ident in self.variables.keys()
    
    def get_global_env(self) -> Env:
        env = self
        while env.parent is not None:
            env = env.parent
        return env

def setup_global_scope():
    from runtime import native_fns
    env = Env()
    # env.assign("print", values.NativeFn(caller = native_fns.print,
    #     args_layout = [
    #         values.Argument("values", "*"),
    #         values.Argument("sep", "Key", " "),
    #         values.Argument("end", "Key", "\n"),
    #         values.Argument("file", "Key", None),
    #         values.Argument("flush", bool, False)
    #     ]
    # ))
    return env