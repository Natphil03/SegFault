from type import *
from AST import *
        
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
            raise Exception(f"Syntax error: Expected {token_type}, got {self.current_token.type}")


    def factor(self):
        token = self.current_token

        if token.type == types.INTEGER:
            self.eat(types.INTEGER)
            return Num(token)
        
        elif token.type == types.STRING:
            self.eat(types.STRING)
            return String(token)
        
        elif token.type == types.TRUE:
            self.eat(types.TRUE)
            return BoolOp(left=None, op=token, right=None)  # Represents `True`

        elif token.type == types.FALSE:
            self.eat(types.FALSE)
            return BoolOp(left=None, op=token, right=None)  # Represents `False`
        
        elif token.type == types.LPAREN:
            self.eat(types.LPAREN)
            node = self.logical_or_expr()
            self.eat(types.RPAREN)
            return node
        
        elif token.type == types.MINUS:
            self.eat(types.MINUS)
            return UnaryOp(token, self.factor())
    
        elif token.type == types.NOT:
            self.eat(types.NOT)
            return UnaryOp(token, self.factor())
        
        else:
            return self.value()
        
    def term(self):
        node = self.factor()
        
        while self.current_token.type in (types.MULTIPLY, types.DIVIDE):
            token = self.current_token

            if token.type == types.MULTIPLY:
                self.eat(types.MULTIPLY)

            elif token.type == types.DIVIDE:
                self.eat(types.DIVIDE)

            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        
        while self.current_token.type in (types.PLUS, types.MINUS):
            token = self.current_token

            if token.type == types.PLUS:
                self.eat(types.PLUS)

            elif token.type == types.MINUS:
                self.eat(types.MINUS)

            node = BinOp(left=node, op=token, right=self.term())
        return node

    def comp_expr(self):
        node = self.expr()
        
        while self.current_token.type in (types.EQUAL, types.NOTEQUAL, types.LESSTHAN, types.GREATERTHAN, types.LESSTHAN_EQUAL, types.GREATERTHAN_EQUAL): 
            token = self.current_token

            if token.type == types.EQUAL:
                self.eat(types.EQUAL)

            elif token.type == types.NOTEQUAL:
                self.eat(types.NOTEQUAL)
                
            elif token.type == types.GREATERTHAN:
                self.eat(types.GREATERTHAN)
            
            elif token.type == types.LESSTHAN:
                self.eat(types.LESSTHAN)
            
            elif token.type == types.GREATERTHAN_EQUAL:
                self.eat(types.GREATERTHAN_EQUAL)
            
            elif token.type == types.LESSTHAN_EQUAL:
                self.eat(types.LESSTHAN_EQUAL)
                
            node = BoolOp(left=node, op=token, right=self.expr())
        return node

    def logical_and_expr(self):
        node = self.comp_expr()

        while self.current_token.type == types.NOT:
            token = self.current_token
            self.eat(types.NOT)
            node = UnaryOp(token, node)  # Apply NOT before moving forward

        return node
    

    def logical_or_expr(self):
        node = self.logical_and_expr()

        while self.current_token.type == types.OR:
            token = self.current_token
            self.eat(types.OR)
            node = BoolOp(left=node, op=token, right=self.logical_and_expr()) 

        return node
    
    def parse(self):
        return self.logical_or_expr()