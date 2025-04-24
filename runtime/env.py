from __future__ import annotations
import typing
import dataclasses
import runtime.values as Value

@dataclasses.dataclass
class VarValue:
    value: Value.RuntimeVal
    constant: bool

class Env:
    def __init__(self, parent: typing.Optional[Env] = None):
        self.parent = parent
        self.variables: typing.Dict[str, VarValue] = {}

    def declare(self, name: str, value: Value.RuntimeVal | None = None, const: bool = False) -> None:
        if name in self.variables:
            raise Exception()
        if const and value is None:
            raise Exception()
        self.variables.setdefault(name, VarValue(value, const))
    
    def assign(self, name: str, value: Value.RuntimeVal) -> Value.RuntimeVal:
        if name in self.variables:
            if self.variables[name]["constant"]:
                raise Exception()
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
        return self.variables[key]
    
    def __setitem__(self, key: str, value: Value.RuntimeVal) -> None:
        self.variables.setdefault(key, value)
    
    def __contains__(self, ident: str) -> bool:
        return ident in self.resolve(ident).variables

def setup_global_scope():
    env = Env()
    # env.assign("print", Value.NativeFn(
    #     caller = print,
    #     args_layout = [
    #         Arg("*values", typing.Any),
    #         Arg("sep", typing.Optional[str], " "),
    #         Arg("end", typing.Optional[str], "\n"),
    #         Arg("file", typing.Optional[typing.Any], None), # TODO: Add support for file
    #         Arg("flush", bool, False) # TODO: Add support for flush
    #     ]
    # ))
    return env