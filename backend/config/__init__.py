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
from backend.config.dataclass import ConfigVersionCls, RootConfigCls
from backend.config.checks import asserting_config_dict

FIELD_ALIASES = {
    "customization": ["customization", "customisation"],
    "customisation": ["customization", "customisation"],
}

LASTEST_VERSION = ConfigVersionCls(major = 2, minor = 1, patch = 1, phase = "indev")
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

def modify_template_option(opt):
    match opt:
        case 0 | "disabled" | False:
            return "disabled"
        case 1 | "enabled" | True:
            return "enabled"
        case 2 | "forced":
            return "forced"
        case _:
            raise errors.InternalError(f"modify_template_option recieve an invalid value: {opt}")

def _solidify_config_dict[T1, T2: dict](cls: type[T1], data: T2) -> T1 | T2:
    """
    Recursively build dataclass instances from nested dictionaries.
    Automatically handles nested dataclasses and missing keys.
    """
    assert dataclasses.is_dataclass(cls)
    if not hasattr(cls, "__dataclass_fields__"):
        return data
    
    kwargs = {}
    type_hints = typing.get_type_hints(cls)

    for field in dataclasses.fields(cls):
        field_name = field.name
        field_type = type_hints.get(field_name, field.type)
        field_value = None
        found_keys = []

        possible_names = FIELD_ALIASES.get(field_name, [field_name])
        for possible_name in possible_names:
            if possible_name in data:
                found_keys.append(possible_name)
                field_value = data[possible_name]
        
        if len(found_keys) > 1:
            raise errors.ConfigError(
                f"Multiple spellings found for field '{field_name}': {found_keys}. "
                f"Use only one of: {possible_names}"
            )
        
        if field_value is not None:
            if hasattr(field_type, "__dataclass_fields__"):
                kwargs[field_name] = _solidify_config_dict(field_type, field_value)
            else:
                kwargs[field_name] = field_value
    
    return cls(**kwargs)

def solidify_config(conf: dict[str, typing.Any]) -> RootConfigCls:
    conf_ = switch_casing(conf)

    try:
        asserting_config_dict(conf_)
    except AssertionError as e:
        raise errors.ConfigError(*e.args)
    
    return typing.cast(RootConfigCls, _solidify_config_dict(RootConfigCls, conf_))
    
    # # ^ Check for identical values
    # redefs: dict[str, list] = {}
    # for k, val in redef.items():
    #     if val is None:
    #         continue
    #     if val not in redefs:
    #         redefs[val] = []
    #     redefs[val].append(k)
    
    # duplicates = [v for v in redefs.values() if len(v) == 2]
    # if duplicates:
    #     if len(duplicates) > 1:
    #         start_msg = "Duplicates have"
    #     else:
    #         start_msg = "Duplicate has"
    #     raise errors.ConfigError(
    #         f"{start_msg} been found: {"; ".join(str(i) for i in duplicates)}"
    #     )
    # del duplicates
    
    # return ConfigCls(
    #     CustomizationCls(
    #         redefine = RedefineCls(
    #             multi_line_comment = MultiLineComment(mtlcs, mtlce),
    #             **redef
    #         ),
    #         integer_base_literals = IntegerBaseLiterals(**int_bases),
    #         **customs
    #     ),
    #     TemplateCls(
    #         **templates
    #     ),
    #     **cus_opts
    # )

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