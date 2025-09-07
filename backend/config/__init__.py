from __future__ import annotations
import json
import jsonschema.exceptions
import jsonschema.validators
import typing
import pathlib
import yaml

from backend import errors
from backend.paths import MAIN_CONFIG_SCHEMA, CONFIG_SUBSCHEMAS
from backend.config.dataclass import *

_SENTINEL = object()
LASTEST_VERSION = ConfigVersionCls(major = ConfOptWrapper(2),
                                   minor = ConfOptWrapper(5),
                                   patch = ConfOptWrapper(0),
                                   phase = ConfOptWrapper("indev"))
CONFIG = RootConfigCls.from_dict({})

def _find_subschema(ref, defs: dict):
    if not isinstance(ref, str):
        return _SENTINEL
    # $ Definition Reference
    if ref.startswith("#/$defs"):
        return {"$ref": ref}
    ref_path = CONFIG_SUBSCHEMAS/ref
    if not ref_path.exists():
        return _SENTINEL
    with open(ref_path) as f:
        ref_schema = _resolve(json.load(f), defs)
        if isinstance(ref_schema, dict) and "$defs" in ref_schema:
            defs.update(ref_schema.pop("$defs"))
        return ref_schema

def _resolve(schema: dict, defs: dict) -> typing.Any:
    if "$ref" in schema:
        ref = _find_subschema(schema["$ref"], defs)
        if ref is not _SENTINEL:
            return ref
    
    schema_ = schema.copy()
    schema_.pop("$comment", None)
    
    for k, v in schema.items():
        if isinstance(v, list):
            schema_[k] = [( _resolve(i, defs) if isinstance(i, dict) else i ) for i in v]
        elif isinstance(v, dict):
            schema_[k] = _resolve(v, defs)
        else:
            schema_[k] = v
    return schema_

def get_schema() -> dict:
    if not MAIN_CONFIG_SCHEMA.exists():
        with open(MAIN_CONFIG_SCHEMA) as f:
            return json.load(f)
    schema_path = CONFIG_SUBSCHEMAS / "main.schema.json"
    if not schema_path.exists():
        raise errors.InternalError(
            "Cannot find the schema to verify the Sapphire config file "
            f"({schema_path})"
        )
    
    # $ Get and modify the schema for just a little bit...
    with open(schema_path) as f:
        defs = {}
        schema = _resolve(json.load(f), defs)
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