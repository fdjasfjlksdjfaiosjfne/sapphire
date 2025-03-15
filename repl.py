import sys; sys.dont_write_bytecode = True
from lexer.lexer import Lexer
from parser.parser import *

while True:
    inpt = input(">>> ")
    print(Parser.produce_ast(Lexer.tokenize(inpt)))