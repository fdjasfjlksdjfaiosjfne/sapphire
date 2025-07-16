from __future__ import annotations
import typing
from dataclasses import dataclass
import runtime.values as values
from backend import errors

@dataclass
class VarValue:
    value: values.RuntimeVal | None
    constant: bool

class Env:
    def __init__(self, parent: typing.Optional[Env] = None):
        self.parent = parent
        self.variables: typing.Dict[str, VarValue] = {}

    def declare(self, name: str, value: values.RuntimeVal | None = None, const: bool = False) -> None:
        if name in self.variables:
            raise errors.VariableError(f"Variable '{name}' is already declared")
        if const and value is None:
            raise errors.SyntaxError("A constant declaration must include a value")
        self.variables.setdefault(name, VarValue(value, const))
    
    def assign(self, name: str, value: values.RuntimeVal) -> None:
        if name in self.variables:
            if self.variables[name].constant:
                raise errors.SyntaxError("Cannot change a constant value")
            setattr(self.variables[name], "value", value)
        self.variables.setdefault(name, VarValue(value, False))
    
    def get(self, name: str) -> values.RuntimeVal:
        env = self.resolve(name)
        var = env.variables.get(name)
        if var is None:
            raise errors.VariableError(f"Variable '{name}' has not been assigned")
        if var.value is None:
            raise errors.VariableError(f"Variable '{name}', although declared, has not been assigned")
        return var.value

    def resolve(self, name: str) -> Env | typing.NoReturn:
        if name in self.variables.keys():
            return self
        if self.parent == None:
            raise Exception()
        return self.parent.resolve(name)
    
    def __getitem__(self, key: str) -> values.RuntimeVal | None:
        return self.variables[key].value
    
    def __setitem__(self, key: str, value: values.RuntimeVal) -> None:
        self.variables.setdefault(key, VarValue(value, False))
    
    def __contains__(self, ident: str) -> bool:
        return ident in self.variables.keys()

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