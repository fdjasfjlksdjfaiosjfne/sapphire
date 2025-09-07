from dataclasses import dataclass
import typing

from backend.config.dataclass.bases import CustomConfDatacls, ConfOptWrapper, _UNFILLED

@dataclass(frozen=True, kw_only=True)
class ClassesConfigCls(CustomConfDatacls):
    syntax: ConfOptWrapper[typing.Literal["class", "cls"]] = ConfOptWrapper(_UNFILLED, "class")

@dataclass(frozen=True, kw_only=True)
class EnumsConfigCls(CustomConfDatacls):
    syntax: ConfOptWrapper[typing.Literal["enum"]] = ConfOptWrapper(_UNFILLED, "enum")

@dataclass(frozen=True, kw_only=True)
class FnArgumentsConfigCls(CustomConfDatacls):
    allow_keyword_arguments: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)
    mutable_value_as_default_behavior: ConfOptWrapper[typing.Literal["copy", "reference"]] = ConfOptWrapper(_UNFILLED, "copy")

@dataclass(frozen = True, kw_only = True)
class FunctionSyntaxConfigCls(CustomConfDatacls):
    keyword: ConfOptWrapper[typing.Literal["fn", "fun", "func", "def", "function"]] = ConfOptWrapper(default = "fn")

@dataclass(frozen=True, kw_only=True)
class FunctionsConfigCls(CustomConfDatacls):
    syntax: FunctionSyntaxConfigCls = FunctionSyntaxConfigCls()
    arguments: FnArgumentsConfigCls = FnArgumentsConfigCls()

@dataclass(frozen=True, kw_only=True)
class ObjectsConfigCls(CustomConfDatacls):
    classes: ClassesConfigCls = ClassesConfigCls()
    enums: EnumsConfigCls = EnumsConfigCls()
    functions: FunctionsConfigCls = FunctionsConfigCls()