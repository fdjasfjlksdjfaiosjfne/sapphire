from __future__ import annotations
import json
import jsonschema.exceptions
import jsonschema.validators
import typing
import pathlib
import yaml

from backend import errors
from backend.paths import MAIN_CONFIG_SCHEMA, CONFIG_SUBSCHEMAS
from backend.config.dataclass import ConfigVersionCls, RootConfigCls

LASTEST_VERSION = ConfigVersionCls(major = 2, minor = 1, patch = 1, phase = "indev") # pyright: ignore[reportArgumentType]

CONFIG = RootConfigCls.from_dict({})

def _resolve_ref(schema: dict, defs: dict) -> typing.Any:
    schema_ = schema.copy()
    schema_.pop("$comment", None)
    for k, v in schema.items():
        if k == "$ref":
            if not isinstance(v, str):
                # $ Let jsonschema throw the error for us
                schema_[k] = v
            if v.startswith("#/$defs"):
                # $ Inline definitions, leave it alone
                schema_[k] = v
            
            ref_path = CONFIG_SUBSCHEMAS / v
            if ref_path.exists():
                with open(ref_path) as f:
                    ref_schema = _resolve_ref(json.load(f), defs)

                    if not isinstance(ref_schema, dict):
                        continue

                    if "$defs" in ref_schema:
                        defs.update(ref_schema.pop("$defs"))
            else:
                # $ Fall back to jsonschema's RefResolver
                schema_[k] = v
        
        elif isinstance(v, list):
            array = []
            for i in v:
                if isinstance(v, dict):
                    array.append(_resolve_ref(i, defs))
                else:
                    array.append(i)
            schema_[k] = array
        elif isinstance(v, dict):
            schema_[k] = _resolve_ref(v, defs)
        else:
            schema_[k] = v
    return schema_

def get_schema() -> dict:
    if MAIN_CONFIG_SCHEMA.exists():
        # $ If the main schema file already exists...
        with open(MAIN_CONFIG_SCHEMA) as f:
            return json.load(f)
    schema_path = CONFIG_SUBSCHEMAS / "main.schema.json"
    if not schema_path.exists():
        raise errors.InternalError(
            "Cannot find the schema to verify the Sapphire config file "
            f"({schema_path})"
        )
    
    # $ Modify the schema for just a little bit...
    with open(schema_path) as f:
        defs = {}
        schema = _resolve_ref(json.load(f), defs)
        schema["$defs"] = defs
    
    # # Processing the schema file every time us
    # * Caching the schema as an actual JSON schema somewhere else
    # * Just remember to regenerate it once changes to the schema are made
    with open(MAIN_CONFIG_SCHEMA, "w", encoding = "utf-8") as f:
        json.dump(schema, f, separators = (",", ":"))
    return schema

def find_config(current_path: pathlib.Path | None = None):
    if current_path == None:
        raise errors.InternalError("get_config_dict() is called without a path, before it is intialized")

    config = {}

    # ^ Finding any config files that may qualify
    acceptable_names = {"sapconfig.json": 0, "sapconfig.yaml": 1}

    # Find matching files and sort by priority
    config_files = sorted(
        (f for f in current_path.parent.iterdir() if f.name in acceptable_names),
        key = lambda p: acceptable_names[p.name]
    )
    schema = get_schema()
    for file in config_files:
        
        with open(file) as f:
            # & Valid JSON is valid YAML, we'll just use the YAML parser
            c_ = yaml.safe_load(f)
            try:
                jsonschema.validators.validate(
                    instance = c_, 
                    schema = schema
                )
            except jsonschema.exceptions.ValidationError as e:
                raise errors.ConfigError(f"Invalid config file\n{e}")
            except jsonschema.exceptions.SchemaError:
                raise errors.InternalError(f"sapconfig.schema.json is faulty")
                    
        config.update(c_)

    global CONFIG
    return (CONFIG := RootConfigCls.from_dict(config))