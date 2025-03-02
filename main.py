from lexer.lexer import Lexer
from parser.parser import Parser

with open(r"C:\Users\Tien Dung\Dropbox\Script\Sapphire\samples\comments.sap") as file:
    lexer = Lexer()
    parser = Parser()
    
    print(parser.produce_ast(lexer.tokenize(file.read())))