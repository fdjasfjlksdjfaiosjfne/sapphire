from __future__ import annotations
from dataclasses import dataclass
from typing import TypedDict
from runtime.values import *

class __(TypedDict):
    value: RuntimeVal
    constant: bool

@dataclass
class Environment:
    def __init__(self, parent: Optional[Environment] = None):
        self.parent = parent
        self.variables: Dict[str, __] = {}

    def declare(self, name: str, value: RuntimeVal, const: bool = False) -> None:
        if name in self.variables:
            raise Exception()
        self.variables.setdefault(name, {"value": value, "constant": const})
    
    @overload
    def assign(self, name: str, value: RuntimeVal, const: bool = False) -> None: ...
    
    @overload
    def assign(self, name: str, value: RuntimeVal, const: bool = False, walrus: Literal[True] = True) -> RuntimeVal: ...
    
    def assign(self, name: str, value: RuntimeVal, const: bool = False, walrus: bool = False) -> None | RuntimeVal:
        env = self.resolve(name)
        if name in env and env.variables[name]["constant"]:
            raise Exception()
        env.variables.setdefault(name, {"value": value, "constant": const})
        return value if walrus else None
    
    def get(self, name: str) -> RuntimeVal:
        env = self.resolve(name)
        return env
    
    def resolve(self, name: str) -> Environment | NoReturn:
        if name in self.variables:
            return self
        if self.parent == None:
            raise Exception()
        return self.parent.resolve(name)
    
    def __getitem__(self, key: str) -> RuntimeVal:
        return self.variables[key]
    
    def __setitem__(self, key: str, value: RuntimeVal) -> None:
        self.variables.setdefault(key, value)
    
    def __contains__(self, value: str) -> bool:
        """
        :)
        """
        return value in self.variables

def setup_global_scope():
    env = Environment()
    
    return env