from interpreter import Interpreter
from lexer import Lexer
from parser import Parser

def main():
    
    src = open("while.sf", "r")
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
