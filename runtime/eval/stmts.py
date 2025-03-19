from parser.nodes import *
from runtime.eval.exprs import *

def eval_program(program: ProgramNode, env: Environment) -> UnusableVal:
    eval_code_block(program.body, env, function = True)
    return UnusableVal