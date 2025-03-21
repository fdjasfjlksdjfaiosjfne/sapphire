import parser.nodes as N
import runtime.eval.exprs as Exprs
import runtime.values as V
from runtime.env import Environment

def eval_program(program: N.ProgramNode, env: Environment) -> None:
    Exprs.eval_code_block(program.body, env)
    return None