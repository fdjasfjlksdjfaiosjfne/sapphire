# Credit to: https://www.youtube.com/playlist?list=PL_2VhOvlMk4UHGqYCLWc6GO8FaPl8fQTh

from lexer.lexer import Lexer
from parser.parser import Parser
from runtime.interpreter import evaluate
from runtime.env import setup_global_scope

global_env = setup_global_scope()

while True:
    # Takes the input
    inpt = input(">>> ")
    
    # Process it
    tkns = Lexer.tokenize(inpt)
    # // print(tkns, end = "\n\n")
    ast_node = Parser.produce_ast(tkns)
    # // print(ast_node, end = "\n\n")
    for i in ast_node.body:
        val = evaluate(i, global_env)
        if val is not None:
            print(repr(val))