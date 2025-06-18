import sys

from jsonschema import validators
from jsonschema.exceptions import ValidationError
import pathlib
import yaml

from parser.lexer import tokenize
from parser.parser import produce_program_ast
from runtime.interpreter import evaluate
from runtime.env import Env

SCHEMA_PATH = r"C:\Users\Tien Dung\Dropbox\Script\Sapphire Family\Sapphire\utils\sapconfig.schema.yaml"


# ~ Type a path here...
# ~ I'm too lazy to setup args 🫠
path = pathlib.Path(input("Path: "))

# ^ Load sapconfig
config_file_exist = False
# ? Find sapconfig.yaml or sapconfig.yml in parent files
for parent in path.parents:
    # $ Check if the sapconfig.yaml or sapconfig.yml exists.
    # $ If both are available, sapconfig.yaml is used
    ## Why? Yes.
    
    config_path = pathlib.Path(str(parent) + r"\sapconfig.yaml")
    if not config_path.exists():
        config_path = pathlib.Path(str(parent) + r"\sapconfig.yml")
        # > If there's neither, just continue searching
        if not config_path.exists(): 
            continue
    config_file_exist = True
    break

# ? Attempt to load the sapconfig file and check it using a schema
if config_file_exist:
    with open(config_path) as config_file:
        with open(SCHEMA_PATH) as schema_file:
            schema = yaml.safe_load(schema_file)
            config = yaml.safe_load(config_file)
            try:
                validators.validate(config, schema)
            except ValidationError:
                print("sapconfig.yaml or sapconfig.yml is invalid.")
                sys.exit(1)

# ^ Reading the code
global_env = Env()
with open(path) as file:
    tokens = tokenize(file.read(), config)
    program_ast = produce_program_ast(tokens)
    evaluate(program_ast, global_env)

# :)