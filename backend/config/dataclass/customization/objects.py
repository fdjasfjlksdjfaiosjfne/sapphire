from dataclasses import dataclass
import typing

from backend.config.baseclasses import CustomDataclass, ConfOptWrapper, _UNFILLED

@dataclass(frozen=True, kw_only=True)
class ClassesConfigCls(CustomDataclass):
    syntax: ConfOptWrapper[typing.Literal["class", "cls"]] = ConfOptWrapper(_UNFILLED, "class")

@dataclass(frozen=True, kw_only=True)
class EnumsConfigCls(CustomDataclass):
    syntax: ConfOptWrapper[typing.Literal["enum"]] = ConfOptWrapper(_UNFILLED, "enum")

@dataclass(frozen=True, kw_only=True)
class FnArgumentsConfigCls(CustomDataclass):
    allow_keyword_arguments: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)
    mutable_value_as_default_behavior: ConfOptWrapper[typing.Literal["copy", "reference"]] = ConfOptWrapper(_UNFILLED, "copy")

@dataclass(frozen = True, kw_only = True)
class FunctionSyntaxConfigCls(CustomDataclass):
    keyword: ConfOptWrapper[typing.Literal["fn", "fun", "func", "def", "function"]] = ConfOptWrapper(default = "fn")

@dataclass(frozen=True, kw_only=True)
class FunctionsConfigCls(CustomDataclass):
    syntax: FunctionSyntaxConfigCls = FunctionSyntaxConfigCls()
    arguments: FnArgumentsConfigCls = FnArgumentsConfigCls()

@dataclass(frozen=True, kw_only=True)
class ObjectsConfigCls(CustomDataclass):
    classes: ClassesConfigCls = ClassesConfigCls()
    enums: EnumsConfigCls = EnumsConfigCls()
    functions: FunctionsConfigCls = FunctionsConfigCls()