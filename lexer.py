from type import *
from sfToken import Token

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self, offset=1):
        self.pos += offset
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def ignore_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
            
        return int(result)

    def check_x_chars(self, num_char_to_check):
        result = ''
        
        for i in range(0, num_char_to_check):
            result += self.text[self.pos + i]
            
        return result
        

    def get_next_token(self):
        while self.current_char is not None:
            self.ignore_whitespace()
            
            if self.current_char is None:
                return Token(types.EOF, None)

            if self.current_char.isdigit():
                return Token(types.INTEGER, self.integer())
            
            if self.current_char == '"':
                self.advance()  # Skip the opening quote
                result = ''
                
                while self.current_char is not None and self.current_char != '"':
                    result += self.current_char
                    self.advance()
                
                if self.current_char == '"':
                    self.advance()  # Skip the closing quote
                else:
                    raise Exception('Unterminated string literal')

                return Token(types.STRING, result)

            if self.current_char == '=' and self.text[self.pos + 1] == '=':
                self.advance(offset=2)
                return Token(types.EQUAL, '==')
            
            if self.current_char == '!' and self.text[self.pos + 1] == '=':
                self.advance(offset=2)
                return Token(types.NOTEQUAL, '!=')
            
            if self.current_char == '!' :
                self.advance()
                return Token(types.NOT, '!')
            
            if self.current_char == '>' and self.text[self.pos + 1] == '=':
                self.advance(offset=2)
                return Token(types.GREATERTHAN_EQUAL, '>=')
            
            if self.current_char == '<' and self.text[self.pos + 1] == '=':
                self.advance(offset=2)
                return Token(types.LESSTHAN_EQUAL, '<=')
            
            if self.current_char == '>':
                self.advance()
                return Token(types.GREATERTHAN, '>')
            
            if self.current_char == '<':
                self.advance()
                return Token(types.LESSTHAN, '<')
            
            if self.current_char == '+':
                self.advance()
                return Token(types.PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(types.MINUS, '-')
            
            if self.current_char == '*':
                self.advance()
                return Token(types.MULTIPLY, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(types.DIVIDE, '/')
            
            if self.current_char == '(': 
                self.advance()
                return Token(types.LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(types.RPAREN, ')')
            
            if self.check_x_chars(4) == 'True' :
                self.advance(offset=4)
                return Token(types.TRUE, 'True')
            
            if self.check_x_chars(5) == 'False' :
                self.advance(offset=5)
                return Token(types.FALSE, 'False')
            
            if self.check_x_chars(3) == 'and' :
                self.advance(offset=3)
                return Token(types.AND, 'and')
            
            if self.check_x_chars(2) == 'or' :
                self.advance(offset=2)
                return Token(types.OR, 'or')
            
            print(self.current_char)
            raise Exception('Invalid character')
        
        return Token(types.EOF, None)