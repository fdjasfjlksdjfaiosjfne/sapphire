from __future__ import annotations

import typing
import pathlib
import jsonschema.exceptions
import jsonschema.validators
import yaml
import regex

import sys, pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent.parent))

from utils._config.conf_dataclasses import (
    CustomizationMode,
    CustomizationCls,
    ConfigCls,
    RedefineCls,
    MultiLineComment,
    IntegerBaseLiterals,
    TemplateCls,
    LASTEST_VERSION,
)

from backend import errors

CAMEL_TO_SNAKE_PATTERN = regex.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

def camel_to_snake(name: str) -> str:
    return CAMEL_TO_SNAKE_PATTERN.sub(r"_\1", name).lower()

def switch_casing(conf: dict) -> dict:
    d = {}
    for k, v in conf.items():
        if isinstance(v, dict):
            d[camel_to_snake(k)] = switch_casing(v)
        else:
            d[camel_to_snake(k)] = v
    return d

def solidify_config(conf: dict[str, typing.Any]) -> ConfigCls:
    conf_ = switch_casing(conf)
    customs: dict[str, typing.Any] = conf_.get("customization", {})
    redef: dict = customs.pop("redefine", {})
    int_bases: dict = customs.pop("integer_base_literals", {})
    config_version: list[int]|str = conf.get("config_version", LASTEST_VERSION)
    cus_opts: dict = conf_.get("custom_options", {})
    templates: dict = conf_.get("template", {})
    mtc: str = redef.pop("multi_line_comment", "/* */")
    mtlcs, mtlce = mtc.split()

    if isinstance(config_version, str):
        config_version = [int(i) for i in config_version.split(".")]
    
    # & I'm not adding multi-version support
    # & What's so important about supporting older development versions anyway?
    # & They just exist for like, a few days at most
    # & I'll add them once it's mainstream...Which is basically never.
    if config_version != LASTEST_VERSION:
        raise errors.InternalError(
            "Due to the developer having an overdose of laziness, version "
            f"{".".join(str(i) for i in config_version)} is not supported. "
            f"Please use version {".".join(str(i) for i in LASTEST_VERSION)} "
            "instead."
        )

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

    templates = {
        k: customization_mode_replace_dict.get(v, CustomizationMode.Disabled) for k, v
        in templates.items()
    }

    customs = typing.cast(dict[str, typing.Any], conf_.get("customization", {}))
    redef: dict = customs.pop("redefine", {})
    int_bases = customs.pop("integer_base_literals", {})

    for american, british in [("mutable_value_assignment_behavior", "mutable_value_assignment_behaviour"), 
                              ("mutable_argument_default_value_behavior", "mutable_argument_default_value_behaviour"), 
                              ("logical_operator_behavior", "logical_operator_behaviour")]:
        if british in customs:
            if american in customs:
                raise errors.ConfigError(
                    "Both the American and British spelling of a configuration"
                    f"('{american}' and '{british}' respectively) is present"
                )
            customs[american] = customs[british]
            del customs[british]

    # ^ Check for identical values
    redef_keys: dict[str, list] = {}
    for k, val in redef.items():
        if val is None:
            continue
        if val in redef_keys:
            redef_keys[val].append(k)
        redef_keys[val] = [k]
    
    duplicates = [v for v in redef_keys.values() if len(v) == 2]
    if duplicates:
        if len(duplicates) > 1:
            start_msg = "Duplicates have"
        else:
            start_msg = "Dupliccate has"
        raise errors.ConfigError(
            f"{start_msg} been found: {"; ".join(str(i) for i in duplicates)}"
        )
    del duplicates

    if int_bases.values() and not any(int_bases.values()):
        raise errors.ConfigError(
            "At least 1 of the integer bases should be allowed"
        )
    
    return ConfigCls(
        CustomizationCls(
            RedefineCls(
                multi_line_comment = MultiLineComment(mtlcs, mtlce),
                **redef
            ),
            integer_base_literals = IntegerBaseLiterals(**int_bases),
            **customs
        ),
        TemplateCls(
            **templates
        ),
        **cus_opts
    )

CONFIG = solidify_config({})

def get_config_dict(current_path: pathlib.Path | None = None):
    global CONFIG

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