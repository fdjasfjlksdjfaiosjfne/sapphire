import typing
from dataclasses import dataclass

from backend.config.dataclass.customization import *

ForcableTemplate: typing.TypeAlias = typing.Literal["disabled", "enabled", "forced"] | object
UnforcableTemplate: typing.TypeAlias = typing.Literal["disabled", "enabled"] | object

@dataclass(frozen=True)
class ConfigVersionCls:
    major: int = 2
    minor: int = 1
    patch: int = 0
    phase: typing.Literal["indev", "alpha",
                          "beta", "release"] = "indev"
    def __repr__(self) -> str:
        return (
            f"<ConfigVersionCls: {self.major}.{self.minor}.{self.patch}"
            f"; phase {self.phase}>"
        )

@dataclass(frozen=True, kw_only=True)
class TemplatesCls:
    inverted_comparisons: ForcableTemplate = NOT_FILLED
    methify: ForcableTemplate = NOT_FILLED

@dataclass(frozen=True, kw_only=True)
class RootConfig:
    customization: CustomizationConfigCls# = CustomizationConfigCls()
    templates: TemplatesCls = TemplatesCls()
    config_version: ConfigVersionCls = ConfigVersionCls()