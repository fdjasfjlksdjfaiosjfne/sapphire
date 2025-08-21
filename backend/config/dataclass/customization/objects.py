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

@dataclass(frozen=True, kw_only=True)
class FunctionsConfigCls(CustomDataclass):
    keyword: ConfigDescriptor[typing.Literal["fn", "fun", "func", "def", "function"]] = ConfigDescriptor(_UNFILLED, "fn")
    arguments: ConfigDescriptor[FnArgumentsConfigCls] = ConfigDescriptor(_UNFILLED, FnArgumentsConfigCls())

@dataclass(frozen=True, kw_only=True)
class ObjectsConfigCls(CustomDataclass):
    classes: ConfigDescriptor[ClassesConfigCls] = ConfigDescriptor(_UNFILLED, ClassesConfigCls())
    enums: ConfigDescriptor[EnumsConfigCls] = ConfigDescriptor(_UNFILLED, EnumsConfigCls())
    functions: ConfigDescriptor[FunctionsConfigCls] = ConfigDescriptor(_UNFILLED, FunctionsConfigCls())