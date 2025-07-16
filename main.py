import pathlib

from parser.parser import Parser
from runtime.interpreter import evaluate
from runtime.env import Env
from backend import errors

# ~ Type a path here...
# & I'm too lazy to setup args
path = pathlib.Path(input("Path: "))

# ^ Reading the code
try:
    global_env = Env()
    with open(path) as file:
        program_ast = Parser(file.read()).parse_module()

        evaluate(program_ast, global_env)
except errors.SapphireError:
    # todo Handle this properly
    raise