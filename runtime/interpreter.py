from values import *
from parser.nodes import *

def evaluate(node: Stmt):
    match node.kind:
        case NodeType.Identifier:
            return 
        case NodeType.Program:
            return 