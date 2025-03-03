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

    def find_integer(self):
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
    
    def find_identifier(self):
        result = ''

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result
    
    def is_float(self):
        temp_text = self.text
        temp_current_pos = self.pos
        
        while temp_text[temp_current_pos] != ';' and temp_text[temp_current_pos] not in operators:
            if temp_text[temp_current_pos] == '.':
                return True

            temp_current_pos +=1    
        return False
    
    def find_float(self):
        result = ''
        
        while self.current_char != ';' and self.current_char not in operators:
            result += self.current_char
            self.advance()
            
        return float(result)
    
    def find_string(self):
        result = ''
        
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        
        if self.current_char == '"':
            self.advance()  # Skip the closing quote
        else:
            raise Exception('Unterminated string literal')

        return result
    
    def handle_word_tokens(self, identifier):
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
            elif identifier == 'bool':
                return Token(types.BOOL_TYPE, 'bool')
            elif identifier == 'float':
                return Token(types.FLOAT_TYPE, 'float')
            elif identifier == 'print':
                return Token(types.PRINT_STMT, 'print')
            elif identifier == 'del':
                return Token(types.DELETE_VAR, 'del')
            elif identifier == 'if':
                return Token(types.IF, 'if')
            elif identifier == 'elseif':
                return Token(types.ELSEIF, 'elseif')
            elif identifier == 'while':
                return Token(types.WHILE, 'while')
            else:
                return Token(types.IDENTIFIER, identifier)  # Variable name or function name
    
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
                if self.is_float():
                    return Token(types.FLOAT, self.find_float())
                else:
                    return Token(types.INTEGER, self.find_integer())
            
            if self.current_char == '"':
                self.advance()  # Skip the opening quote
                result = self.find_string()
                return Token(types.STRING, result)

            identifier = self.find_identifier()
            
            if identifier:
                return self.handle_word_tokens(identifier)
            
            if self.check_x_chars(2) == '==':
                self.advance(offset=2)
                return Token(types.EQUAL, '==')
            
            elif self.current_char == '=':
                self.advance()
                return Token(types.ASSIGN, '=')
            
            elif self.check_x_chars(2) == '!=':
                self.advance(offset=2)
                return Token(types.NOTEQUAL, '!=')
            
            elif self.current_char == '!':
                self.advance()
                return Token(types.NOT, '!')
            
            elif self.check_x_chars(2) == '>=':
                self.advance(offset=2)
                return Token(types.GREATERTHAN_EQUAL, '>=')
            
            elif self.check_x_chars(2) == '<=':
                self.advance(offset=2)
                return Token(types.LESSTHAN_EQUAL, '<=')
            
            elif self.current_char == '>':
                self.advance()
                return Token(types.GREATERTHAN, '>')
            
            elif self.current_char == '<':
                self.advance()
                return Token(types.LESSTHAN, '<')
            
            elif self.current_char == '+':
                self.advance()
                return Token(types.PLUS, '+')
            
            elif self.current_char == '-':
                self.advance()
                return Token(types.MINUS, '-')
            
            elif self.current_char == '*':
                self.advance()
                return Token(types.MULTIPLY, '*')
            
            elif self.current_char == '/':
                self.advance()
                return Token(types.DIVIDE, '/')
            
            elif self.current_char == '(': 
                self.advance()
                return Token(types.LPAREN, '(')
            
            elif self.current_char == ')':
                self.advance()
                return Token(types.RPAREN, ')')
            
            elif self.current_char == '{':
                self.advance()
                return Token(types.CB_OPEN, '{')
                        
            elif self.current_char == '}':
                self.advance()
                return Token(types.CB_CLOSE, '}')
            
            raise Exception('Invalid character')
        
        return Token(types.EOF, None)