from dataclasses import dataclass
import typing

from backend.config.baseclasses import CustomDataclass, ConfigDescriptor, _UNFILLED

@dataclass(frozen=True, kw_only=True)
class ClassesConfigCls(CustomDataclass):
    syntax: ConfigDescriptor[typing.Literal["class", "cls"]] = ConfigDescriptor(_UNFILLED, "class")

@dataclass(frozen=True, kw_only=True)
class EnumsConfigCls(CustomDataclass):
    syntax: ConfigDescriptor[typing.Literal["enum"]] = ConfigDescriptor(_UNFILLED, "enum")

@dataclass(frozen=True, kw_only=True)
class FnArgumentsConfigCls(CustomDataclass):
    allow_keyword_arguments: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    mutable_value_as_default_behavior: ConfigDescriptor[typing.Literal["copy", "reference"]] = ConfigDescriptor(_UNFILLED, "copy")

@dataclass(frozen = True, kw_only = True)
class FunctionSyntaxConfigCls(CustomDataclass):
    keyword: ConfigDescriptor[typing.Literal["fn", "fun", "func", "def", "function"]] = ConfigDescriptor(default = "fn")

@dataclass(frozen=True, kw_only=True)
class FunctionsConfigCls(CustomDataclass):
    syntax: FunctionSyntaxConfigCls = FunctionSyntaxConfigCls()
    arguments: FnArgumentsConfigCls = FnArgumentsConfigCls()

@dataclass(frozen=True, kw_only=True)
class ObjectsConfigCls(CustomDataclass):
    classes: ClassesConfigCls = ClassesConfigCls()
    enums: EnumsConfigCls = EnumsConfigCls()
    functions: FunctionsConfigCls = FunctionsConfigCls()