from dataclasses import dataclass
import typing

from backend.config.baseclasses import CustomDataclass

@dataclass(frozen=True, kw_only=True)
class ClassesConfigCls(CustomDataclass):
    syntax: typing.Literal["class", "cls"] = "class"

@dataclass(frozen=True, kw_only=True)
class EnumsConfigCls(CustomDataclass):
    syntax: typing.Literal["enum"] = "enum"


@dataclass(frozen=True, kw_only=True)
class FnArgumentsConfigCls(CustomDataclass):
    allow_keyword_arguments: bool = True
    mutable_value_as_default_behavior: typing.Literal["copy", "reference"] = "copy"

@dataclass(frozen=True, kw_only=True)
class FunctionsConfigCls(CustomDataclass):
    keyword: typing.Literal["fn", "fun", "func", "def", "function"] = "fn"
    arguments: FnArgumentsConfigCls = FnArgumentsConfigCls()

@dataclass(frozen=True, kw_only=True)
class ObjectsConfigCls(CustomDataclass):
    classes: ClassesConfigCls = ClassesConfigCls()
    enums: EnumsConfigCls = EnumsConfigCls()
    functions: FunctionsConfigCls = FunctionsConfigCls()