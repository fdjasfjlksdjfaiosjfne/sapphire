from __future__ import annotations
from enum import Enum, auto
import typing
import pathlib
import jsonschema.exceptions
import jsonschema.validators
import yaml
import types
import regex
from dataclasses import dataclass

from backend import errors

class CustomizationMode(Enum):
    Disabled = 0
    Enabled = 1
    Forced = 2

@dataclass(frozen = True)
class RedefineCls:
    not_equal: typing.Literal["<>", "><", "!="] = "!="
    function_def: typing.Literal["def", "fn", "fun", "func", "function"] = "fn"
    class_def: typing.Literal["class", "cls"] = "class"
    else_if: typing.Literal["else if", "elseif", "elsif", "elif"] = "elif"
    spaceship_operator: typing.Literal["<=>", ">=<"] = "<=>"

@dataclass(frozen = True)
class LangCustomizationCls:
    redefine: RedefineCls = RedefineCls()
    code_blocks: typing.Literal["braces", "indentation", "end"] = "braces"
    operator_notation: typing.Literal["infix", "prefix", "postfix"] = "infix"
    oop_model: typing.Literal["hybrid", "class", "prototype"] = "class"
    forced_encapsulation: bool = True
    encapsulation_method: typing.Literal["pythonic", "enforced"] = "enforced"
    default_case_notation: typing.Literal["*", "_", "default"] = "_"
    logical_operator_behavior: typing.Literal["boolean_only", "pythonic", "extended_pythonic"] = "extended_pythonic"
    allow_booleans: bool = True
    allow_null: bool = True
    case_insensitive_booleans: bool = True
    case_insensitive_null: bool = True
    mutable_value_assignment_behavior: typing.Literal["copy", "reference"] = "copy"
    mutable_argument_default_value_behavior: typing.Literal["copy", "reference"] = "copy"

@dataclass(frozen = True)
class LangModeCls:
    inverted_operators: CustomizationMode = CustomizationMode.Disabled
    methify: CustomizationMode = CustomizationMode.Disabled

@dataclass(frozen = True)
class ConfigCls:
    language_customization: LangCustomizationCls = LangCustomizationCls()
    language_customization_modes: LangModeCls = LangModeCls()
    custom_options: dict = {}

CAMEL_TO_SNAKE_PATTERN = regex.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

def camel_to_snake(name: str):
    return CAMEL_TO_SNAKE_PATTERN.sub(r"_\1", name).lower()

def solidify_config(conf: dict) -> ConfigCls:

    # ^ languageCustomizationModes
    customization_mode_replace_dict = {
        "disabled": CustomizationMode.Disabled,
        "enabled": CustomizationMode.Enabled,
        "forced": CustomizationMode.Forced,

        0: CustomizationMode.Disabled,
        1: CustomizationMode.Enabled,
        2: CustomizationMode.Forced,

        False: CustomizationMode.Disabled,
        True: CustomizationMode.Enabled,
    }
    conf["languageCustomizationModes"] = {
        k: customization_mode_replace_dict.get(v, CustomizationMode.Disabled) for k, v
        in conf["languageCustomizationModes"].items()
    }

    lang_custom = typing.cast(dict[str, typing.Any], conf["languageCustomization"].copy())
    lang_custom.pop("redefine")

    # ^ Check for duplicates
    for american, british in [("mutableValueAssignmentBehavior", "mutableValueAssignmentBehaviour"), 
                              ("mutableArgumentDefaultValueBehavior", "mutableArgumentDefaultValueBehaviour"), 
                              ("logicalOperatorBehavior", "logicalOperatorBehaviour")]:
        if british in lang_custom["languageCustomization"]:
            if american in lang_custom["languageCustomization"]:
                raise errors.ConfigError(
                    "Both the American and British spelling of a configuration"
                    f"('{american}' and '{british}' respectively) is present"
                )
            lang_custom[american] = lang_custom[british]
            del lang_custom[british]

    return ConfigCls(
        LangCustomizationCls(
            RedefineCls(**conf["languageCustomization"]["redefine"]),
            **lang_custom
        ),
        LangModeCls(
            **conf["languageCustomizationModes"]
        ),
        conf["customOptions"]
    )

CONFIG = None

def get_config_dict(current_path: pathlib.Path | None = None):
    global CONFIG

    if CONFIG is not None:
        return CONFIG
    
    if current_path == None:
        raise errors.InternalError("get_config_dict() is called without a path, before it is intialized")

    config = {}

    # ^ Finding any config files that may qualify
    config_files = []
    acceptable_names = {"sapconfig.json": 0, "sapconfig.yaml": 1}

    for parent in reversed(current_path.parents):
        # Find matching files and sort by priority
        matches = sorted(
            (f for f in parent.iterdir() if f.name in acceptable_names),
            key = lambda p: acceptable_names[p.name]
        )
        config_files.extend(matches)
    
    for file in config_files:
        with open(pathlib.Path(__file__).parent / "utils" / "sapconfig.schema.json") as schema_file:
            # & Valid JSON is valid YAML, just use the YAML parser
            schema = yaml.safe_load(schema_file)
            with open(file) as f:
                c_ = yaml.safe_load(f)
                try:
                    jsonschema.validators.validate(c_, schema)
                except jsonschema.exceptions.ValidationError as e:
                    raise errors.ConfigError(f"Invalid config file\n{e}")
                except jsonschema.exceptions.SchemaError:
                    raise errors.InternalError(f"sapconfig.schema.json is faulty")
                    
        config.update(c_)
    
    return (CONFIG := solidify_config(config))