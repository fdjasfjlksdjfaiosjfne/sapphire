from __future__ import annotations
import typing
from dataclasses import dataclass
import runtime.values as Value
from backend import errors

@dataclass
class VarValue:
    value: Value.RuntimeVal
    constant: bool

class Env:
    def __init__(self, parent: typing.Optional[Env] = None):
        self.parent = parent
        self.variables: typing.Dict[str, VarValue] = {}

    def declare(self, name: str, value: Value.RuntimeVal | None = None, const: bool = False) -> None:
        if name in self.variables:
            raise errors.VariableError(f"Variable '{name}' is already declared")
        if const and value is None:
            raise errors.SyntaxError("A constant declaration must include a value")
        self.variables.setdefault(name, VarValue(value, const))
    
    def assign(self, name: str, value: Value.RuntimeVal) -> Value.RuntimeVal:
        if name in self.variables:
            if self.variables[name].constant:
                raise errors.SyntaxError("Cannot change a constant value")
            setattr(self.variables[name], "value", value)
        self.variables.setdefault(name, VarValue(value, False))
    
    def get(self, name: str) -> Value.RuntimeVal:
        env = self.resolve(name)
        return env.variables.get(name).value
    
    def resolve(self, name: str) -> Env | typing.NoReturn:
        if name in self.variables.keys():
            return self
        if self.parent == None:
            raise Exception()
        return self.parent.resolve(name)
    
    def __getitem__(self, key: str) -> Value.RuntimeVal:
        return self.variables[key].value
    
    def __setitem__(self, key: str, value: Value.RuntimeVal) -> None:
        self.variables.setdefault(key, value)
    
    def __contains__(self, ident: str) -> bool:
        return ident in self.variables.keys()

def setup_global_scope():
    env = Env()
    env.assign("print", Value.NativeFn(
        caller = print,
        args_layout = [
            Value.Argument("values", "*"),
            Value.Argument("sep", "Key", " "),
            Value.Argument("end", "Key", "\n"),
            Value.Argument("file", "Key", None),
            Value.Argument("flush", bool, False)
        ]
    ))
    return env