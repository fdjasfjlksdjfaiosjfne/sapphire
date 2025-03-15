import sys; sys.dont_write_bytecode = True
from lexer.lexer import Lexer
from parser.parser import *

with open(r"C:\Users\Tien Dung\Dropbox\Script\Sapphire\samples\comments.sap") as file:
    lexer = Lexer()
    
    print(Parser.produce_ast(lexer.tokenize(file.read())))