from datatypes import *

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class BoolOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr
        
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        
        elif token.type == STRING:
            self.eat(STRING)
            return String(token)
        
        elif token.type == TRUE:
            self.eat(TRUE)
            return BoolOp(left=None, op=token, right=None)  # Represents `True`

        elif token.type == FALSE:
            self.eat(FALSE)
            return BoolOp(left=None, op=token, right=None)  # Represents `False`
        
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnaryOp(token, self.factor())

    def term(self):
        node = self.factor()
        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token

            if token.type == MULTIPLY:
                self.eat(MULTIPLY)

            elif token.type == DIVIDE:
                self.eat(DIVIDE)

            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token

            if token.type == PLUS:
                self.eat(PLUS)

            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())
        return node

    def comp_expr(self):
        node = self.expr()
        
        while self.current_token.type in (EQUAL, NOTEQUAL, LESSTHAN, GREATERTHAN, LESSTHAN_EQUAL, GREATERTHAN_EQUAL): 
            token = self.current_token

            if token.type == EQUAL:
                self.eat(EQUAL)

            elif token.type == NOTEQUAL:
                self.eat(NOTEQUAL)
                
            elif token.type == GREATERTHAN:
                self.eat(GREATERTHAN)
            
            elif token.type == LESSTHAN:
                self.eat(LESSTHAN)
            
            elif token.type == GREATERTHAN_EQUAL:
                self.eat(GREATERTHAN_EQUAL)
            
            elif token.type == LESSTHAN_EQUAL:
                self.eat(LESSTHAN_EQUAL)
                
            node = BoolOp(left=node, op=token, right=self.expr())
        return node

    def logical_and_expr(self):
        node = self.comp_expr()

    
        return node
    

    def logical_or_expr(self):
        node = self.logical_and_expr()

    
        return node
    
    def parse(self):
        return self.logical_or_expr()