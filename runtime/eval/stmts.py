import parser.nodes as N
import runtime.eval.exprs as Exprs
import runtime.values as V
from env import Environment

def eval_program(program: V.ProgramNode, env: Environment) -> V.UnusableVal:
    Exprs.eval_code_block(program.body, env, function = True)
    return V.UnusableVal()