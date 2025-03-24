from __future__ import annotations
from dataclasses import dataclass
from typing import TypedDict, Optional, overload, Dict, Literal, NoReturn
import runtime.values as Value

class __(TypedDict):
    value: Value.RuntimeVal
    constant: bool

@dataclass
class Env:
    def __init__(self, parent: Optional[Env] = None):
        self.parent = parent
        self.variables: Dict[str, __] = {}

    def declare(self, name: str, value: Value.RuntimeVal | None = None, const: bool = False) -> None:
        if name in self.variables:
            raise Exception()
        if const and value is None:
            raise Exception()
        self.variables.setdefault(name, {"value": value, "constant": const})
    
    def assign(self, name: str, value: Value.RuntimeVal) -> Value.RuntimeVal:
        if name in self and self.variables[name]["constant"]:
            raise Exception()
        self.variables.setdefault(name, {"value": value, "constant": False})
    
    def get(self, name: str) -> Value.RuntimeVal:
        env = self.resolve(name)
        return env
    
    def resolve(self, name: str) -> Env | NoReturn:
        if name in self.variables:
            return self
        if self.parent == None:
            raise Exception()
        return self.parent.resolve(name)
    
    def __getitem__(self, key: str) -> Value.RuntimeVal:
        return self.variables[key]
    
    def __setitem__(self, key: str, value: Value.RuntimeVal) -> None:
        self.variables.setdefault(key, value)
    
    def __contains__(self, ident: str) -> bool:
        """
        :)
        """
        
        return ident in self.resolve(ident).variables

def setup_global_scope():
    env = Env()
    env.assign("print", Value.NativeFn())
    return env