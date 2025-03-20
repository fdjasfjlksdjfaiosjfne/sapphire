from __future__ import annotations
from dataclasses import dataclass
from typing import TypedDict, Optional, overload, Dict, Literal, NoReturn
import runtime.values as V

class __(TypedDict):
    value: V.RuntimeVal
    constant: bool

@dataclass
class Environment:
    def __init__(self, parent: Optional[Environment] = None):
        self.parent = parent
        self.variables: Dict[str, __] = {}

    def declare(self, name: str, value: V.RuntimeVal, const: bool = False) -> None:
        if name in self.variables:
            raise Exception()
        self.variables.setdefault(name, {"value": value, "constant": const})
    
    @overload
    def assign(self, name: str, value: V.RuntimeVal, const: bool = False) -> None: ...
    
    @overload
    def assign(self, name: str, value: V.RuntimeVal, const: bool = False, walrus: Literal[True] = True) -> V.RuntimeVal: ...
    
    def assign(self, name: str, value: V.RuntimeVal, const: bool = False, walrus: bool = False) -> None | V.RuntimeVal:
        env = self.resolve(name)
        if name in env and env.variables[name]["constant"]:
            raise Exception()
        env.variables.setdefault(name, {"value": value, "constant": const})
        return value if walrus else None
    
    def get(self, name: str) -> V.RuntimeVal:
        env = self.resolve(name)
        return env
    
    def resolve(self, name: str) -> Environment | NoReturn:
        if name in self.variables:
            return self
        if self.parent == None:
            raise Exception()
        return self.parent.resolve(name)
    
    def __getitem__(self, key: str) -> V.RuntimeVal:
        return self.variables[key]
    
    def __setitem__(self, key: str, value: V.RuntimeVal) -> None:
        self.variables.setdefault(key, value)
    
    def __contains__(self, value: str) -> bool:
        """
        :)
        """
        return value in self.variables

def setup_global_scope():
    env = Environment()
    
    return env