from type import *
from sfToken import Token

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.tokens = []

    def lex(self):
        while self.pos + 1 <= len(self.text):
            self.tokens.append(self.get_next_token())

        return self.tokens

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
    
    def identifier(self):
        result = ''

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self):
        
        while self.current_char is not None:
            self.ignore_whitespace()
            
            if self.current_char is None:
                self.advance()  
                return Token(types.EOF, None) # end of file

            if self.current_char == ';':
                self.advance()
                return Token(types.SEMI_COLON, ';')

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

            identifier = self.identifier()

            if identifier:
                if identifier == 'True':
                    return Token(types.TRUE, 'True')
                elif identifier == 'False':
                    return Token(types.FALSE, 'False')
                elif identifier == 'and':
                    return Token(types.AND, 'and')
                elif identifier == 'or':
                    return Token(types.OR, 'or')
                elif identifier == 'int':
                    return Token(types.INTEGER_TYPE, 'int')
                elif identifier == 'string':
                    return Token(types.STRING_TYPE, 'string')
                elif identifier == 'print':
                    return Token(types.PRINT_STMT, 'print')
                elif identifier == 'del':
                    return Token(types.DELETE_VAR, 'del')
                else:
                    return Token(types.IDENTIFIER, identifier)  # Variable name or function name
            
            if self.check_x_chars(2) == '==':
                self.advance(offset=2)
                return Token(types.EQUAL, '==')
            
            if self.current_char == '=':
                self.advance()
                return Token(types.ASSIGN, '=')
            
            if self.check_x_chars(2) == '!=':
                self.advance(offset=2)
                return Token(types.NOTEQUAL, '!=')
            
            if self.current_char == '!':
                self.advance()
                return Token(types.NOT, '!')
            
            if self.check_x_chars(2) == '>=':
                self.advance(offset=2)
                return Token(types.GREATERTHAN_EQUAL, '>=')
            
            if self.check_x_chars(2) == '<=':
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
            
            raise Exception('Invalid character')
        
        return Token(types.EOF, None)