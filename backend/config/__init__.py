from __future__ import annotations
import dataclasses
import dotenv_vault
import os
import jsonschema.exceptions
import jsonschema.validators
import typing
import pathlib
import sys
import yaml
import regex

dotenv_vault.load_dotenv()
sys.path.insert(0, os.getenv("ROOT_PATH") or "")

from backend import errors
from backend.config.dataclass import (
    ConfigVersionCls,

)

LASTEST_VERSION = ConfigVersionCls(2, 0, 0, "indev")
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
    if "customization" in conf_ and "customisation" in conf_:
        raise errors.ConfigError(
            "Both the American and British spelling of a configuration option"
            f"('customization' and 'customisation' respectively) is present"
        )
    customs: dict[str, typing.Any] = conf_.pop("customization", conf_.pop("customisation", {}))
    redef: dict = customs.pop("redefine", {})
    int_bases: dict = customs.pop("integer_base_literals", {})
    config_version: dict = conf_.pop("config_version", LASTEST_VERSION)
    cus_opts: dict = conf_.get("custom_options", {})
    templates: dict = conf_.get("template", {})
    mtc: str = redef.pop("multi_line_comment", "/* */")
    mtlcs, mtlce = mtc.split()
    
    # & I'm not adding multi-version support
    # & What's so important about supporting older development versions anyway?
    # & They just exist for like, a few days at most
    # & I'll add them once it's mainstream...Which is basically never.
    if config_version != dataclasses.asdict(LASTEST_VERSION):
        raise errors.InternalError(
            "Due to the developer having an overdose of laziness, version "
            f"{".".join(str(i) for i in config_version)} is not supported. "
            f"Please use version {".".join(str(i) for i in dataclasses.astuple(LASTEST_VERSION))} "
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

    for american, british in [("mutable_value_assignment_behavior", "mutable_value_assignment_behaviour"), 
                              ("mutable_argument_default_value_behavior", "mutable_argument_default_value_behaviour"), 
                              ("logical_operator_behavior", "logical_operator_behaviour")]:
        if british in customs:
            if american in customs:
                raise errors.ConfigError(
                    "Both the American and British spelling of a configuration option"
                    f"('{american}' and '{british}' respectively) is present"
                )
            customs[american] = customs[british]
            del customs[british]

    # ^ Check for identical values
    redefs: dict[str, list] = {}
    for k, val in redef.items():
        if val is None:
            continue
        if val not in redefs:
            redefs[val] = []
        redefs[val].append(k)
    
    duplicates = [v for v in redefs.values() if len(v) == 2]
    if duplicates:
        if len(duplicates) > 1:
            start_msg = "Duplicates have"
        else:
            start_msg = "Duplicate has"
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
            redefine = RedefineCls(
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

#CONFIG = solidify_config({})

def get_resolver():
    main_schema_dir = pathlib.Path("./schemas").resolve()
    if not main_schema_dir.exists():
        raise errors.InternalError(
            "..."
        )
    base_uri = main_schema_dir.as_uri() + "/"

    def load_file(uri):
        if uri.startswith("file://"):
            file_path = pathlib.Path(uri[7:])
        else:
            file_path = main_schema_dir / uri
        
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    resolver = jsonschema.validators.RefResolver(
        base_uri = base_uri,
        referrer = {},
        handlers = {"file": load_file}
    )

    return resolver

def get_config(current_path: pathlib.Path | None = None):
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
        schema_path = (pathlib.Path(__file__).parent / "schemas" / "main.schema.json").resolve()
        if not schema_path.exists():
            raise errors.InternalError(
                "Cannot find the schema to verify the Sapphire config file "
                f"({schema_path})"
            )
        with open(schema_path) as schema_file:
            # & Valid JSON is valid YAML, I'll just use the YAML parser
            schema = yaml.safe_load(schema_file)
            with open(file) as f:
                c_ = yaml.safe_load(f)
                try:
                    jsonschema.validators.validate(
                        instance = c_, 
                        schema = schema,
                        resolver = get_resolver()
                    )
                except jsonschema.exceptions.ValidationError as e:
                    raise errors.ConfigError(f"Invalid config file\n{e}")
                except jsonschema.exceptions.SchemaError:
                    raise errors.InternalError(f"sapconfig.schema.json is faulty")
                    
        config.update(c_)

    return (CONFIG := solidify_config(config))