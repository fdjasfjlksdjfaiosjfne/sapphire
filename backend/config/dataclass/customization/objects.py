from dataclasses import dataclass
import typing

from backend.config.baseclasses import custom_dataclass

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ClassesConfigCls:
    syntax: typing.Literal["class", "cls"] = "class"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class EnumsConfigCls:
    syntax: typing.Literal["enum"] = "enum"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class FnArgumentsConfigCls:
    allow_keyword_arguments: bool = True
    mutable_value_as_default_behavior: typing.Literal["copy", "reference"] = "copy"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class FunctionsConfigCls:
    keyword: typing.Literal["fn", "fun", "func", "def", "function"] = "fn"
    arguments: FnArgumentsConfigCls = FnArgumentsConfigCls()

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ObjectsConfigCls:
    classes: ClassesConfigCls = ClassesConfigCls()
    enums: EnumsConfigCls = EnumsConfigCls()
    functions: FunctionsConfigCls = FunctionsConfigCls()