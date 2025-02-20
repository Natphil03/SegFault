INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN, EOF, NEGATE = 'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LPAREN', 'RPAREN', 'EOF', 'NEGATE'
OPERATORS = {PLUS: 1, MINUS: 1, MULTIPLY: 2, DIVIDE: 2}  # Operator precedence
TYPES = {INTEGER}

class Token:
    def __init__(self, type, value, subtype = None):
        self.type = type
        self.value = value
        self.subtype = subtype

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)}, {repr(self.subtype)})'

    def __repr__(self):
        return self.__str__()

class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        """Move position forward and update current_char"""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def ignore_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def find_full_integer(self):
        """Extracts multi-digit integer from input"""
        str_int = ""

        while self.current_char is not None and self.current_char.isdigit():
            str_int += self.current_char
            self.advance()

        return int(str_int)

    def get_next_token(self):
        """Lexical analyzer that tokenizes the input"""
        while self.current_char is not None:
            self.ignore_whitespace()
            print(self.current_char)
            if self.current_char is None:
                return Token(EOF, None)
            
            if self.current_char == '-':
                self.advance()
                
                if self.current_char is not None and self.current_char.isdigit():
                    return Token(INTEGER, self.find_full_integer(), NEGATE)

                elif self.current_char in {' ', '(', ')', '*', '/', '+', '-', EOF}:  # It's a subtraction operator
                    return Token(MINUS, '-')

                
            if self.current_char.isdigit():
                return Token(INTEGER, self.find_full_integer())

            elif self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            elif self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            
            elif self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')

            elif self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')

            elif self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            elif self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)

    def get_expression(self):
        """Convert the input into Reverse Polish Notation (RPN) using the Shunting-Yard Algorithm"""
        output_queue = []
        operator_stack = []

        self.current_token = self.get_next_token()

        while self.current_token.type != EOF:
            
            if self.current_token.type == INTEGER:
                if self.current_token.subtype == NEGATE:
                    output_queue.append(Token(INTEGER, -self.current_token.value))
                else:
                    output_queue.append(self.current_token)

            elif self.current_token.type in OPERATORS:
                # Handle operator precedence
                while (operator_stack and 
                    operator_stack[-1].type in OPERATORS and 
                    OPERATORS[operator_stack[-1].type] >= OPERATORS[self.current_token.type]):
                    output_queue.append(operator_stack.pop())

                operator_stack.append(self.current_token)

            elif self.current_token.type == LPAREN:
                # Left parenthesis, just push to stack
                operator_stack.append(self.current_token)

            elif self.current_token.type == RPAREN:
                # Right parenthesis, pop from stack until left parenthesis is found
                while operator_stack and operator_stack[-1].type != LPAREN:
                    output_queue.append(operator_stack.pop())
                    
                if not operator_stack:
                    self.error()  # Mismatched parentheses

                operator_stack.pop()  # Pop the '(' from stack

            self.current_token = self.get_next_token()

        # After reading all tokens, pop remaining operators from the stack
        while operator_stack:
            if operator_stack[-1].type in {LPAREN, RPAREN}:
                self.error()  # Mismatched parentheses
            output_queue.append(operator_stack.pop())

        return output_queue


    def compute(self):
        """Evaluate the expression in RPN format using a stack"""
        rpn_expression = self.get_expression()
        print(rpn_expression)
        operand_stack = []

        for token in rpn_expression:

            if token.type == INTEGER:
                operand_stack.append(token.value)
            
            elif token.type in OPERATORS:
                if len(operand_stack) < 2:
                    self.error()  # Not enough operands 

                right = operand_stack.pop()
                left = operand_stack.pop()

                if token.type == PLUS:
                    operand_stack.append(left + right)

                elif token.type == MINUS:
                    operand_stack.append(left - right)
                
                elif token.type == MULTIPLY:
                    operand_stack.append(left * right)
                
                elif token.type == DIVIDE:
                    operand_stack.append(left / right)

        if len(operand_stack) != 1:
            self.error()  # Invalid expression

        return operand_stack[0]

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break

        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.compute()
        print(result)

if __name__ == '__main__':
    main()
