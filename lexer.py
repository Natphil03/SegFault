from datatypes import *
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

    def get_next_token(self):
        while self.current_char is not None:
            self.ignore_whitespace()
            
            if self.current_char is None:
                return Token(EOF, None)

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.current_char == '"':
                self.advance()  # Skip the opening quote
                result = ''
                
                while self.current_char is not None and self.current_char != '"':
                    result += self.current_char
                    self.advance()
                
                if self.current_char == '"':
                    self.advance()  # Consume the closing quote
                else:
                    raise Exception('Unterminated string literal')

                return Token(STRING, result)

            if self.current_char == '=' and self.text[self.pos + 1] == '=':
                self.advance(offset=2)
                return Token(EQUAL, '==')
            
            if self.current_char == '!' and self.text[self.pos + 1] == '=':
                self.advance(offset=2)
                return Token(NOTEQUAL, '!=')
            
            if self.current_char == '>' and self.text[self.pos + 1] == '=':
                self.advance(offset=2)
                return Token(GREATERTHAN_EQUAL, '>=')
            
            elif self.current_char == '<' and self.text[self.pos + 1] == '=':
                self.advance(offset=2)
                return Token(LESSTHAN_EQUAL, '<=')
            
            elif self.current_char == '>':
                self.advance()
                return Token(GREATERTHAN, '>')
            
            elif self.current_char == '<':
                self.advance()
                return Token(LESSTHAN, '<')
            
        
            
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            
            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')
            
            if self.current_char == '(': 
                self.advance()
                return Token(LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            raise Exception('Invalid character')
        
        return Token(EOF, None)