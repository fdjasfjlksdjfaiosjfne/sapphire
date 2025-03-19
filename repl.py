# Credit to: https://www.youtube.com/playlist?list=PL_2VhOvlMk4UHGqYCLWc6GO8FaPl8fQTh

import sys; sys.dont_write_bytecode = True
from lexer.lexer import Lexer
from parser.parser import *
from runtime.interpreter import evaluate
from runtime.env import *

while True:
    global_env = setup_global_scope()
    inpt = input(">>> ")
    tkns = Lexer.tokenize(inpt)
    print(tkns, end = "\n\n")
    ast_node = Parser.produce_ast(tkns)
    print(ast_node, end = "\n\n")
    evaluate(ast_node, global_env)