from __future__ import annotations
import jsonschema.exceptions
import jsonschema.validators
import typing
import pathlib
import yaml

from backend import errors
from backend.paths import ROOT
from backend.config.dataclass import ConfigVersionCls, RootConfigCls

LASTEST_VERSION = ConfigVersionCls(major = 2, minor = 1, patch = 1, phase = "indev") # pyright: ignore[reportArgumentType]

CONFIG = RootConfigCls.from_dict({})

def get_resolver():
    main_schema_dir = (ROOT / "backend" / "config" / "schemas").resolve()
    if not main_schema_dir.exists():
        raise errors.InternalError(
            "The directory that is used to store schemas for the configuration files "
            f"({main_schema_dir}) does not exist"
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

    global CONFIG
    return (CONFIG := RootConfigCls.from_dict(config))