from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
import sys

def main():
    if len(sys.argv) > 1:
        src = open(sys.argv[1], "r")
    else:
        src = open("nested while.sf", "r")
    
    
    content = src.read()
    # print(content)
    
    lexer = Lexer(content)
    tokens = lexer.lex()
    # print(tokens)
    
    parser = Parser(tokens)
    AST = parser.parse()
    # print(AST)

    interpreter = Interpreter(AST)
    interpreter.interpret()
    
    
if __name__ == '__main__':
    main()
