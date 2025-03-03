from type import *
from AST import *
import time

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.AST_root = AST()

    def advance_token(self):
        self.pos += 1
        
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos] 
 
    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance_token()
        else:
            raise Exception(f"Syntax error: Expected {token_type}, got {self.current_token.type}")

    def value(self):
        token = self.current_token

        if token.type == types.IDENTIFIER:
            self.eat(types.IDENTIFIER)
            return Identifier(token)  
        
    def declaration(self):
        type_var = self.current_token
        self.eat(type_var.type) # this is kinda wrong

        iden = self.current_token
        self.eat(types.IDENTIFIER)

        assign_token = self.current_token
        self.eat(types.ASSIGN)

        val = self.logical_or_expr()

        self.eat(types.SEMI_COLON)
        return DeclarationOp(type=type_var, left=iden, op=assign_token, right=val)  # Create an AST node for assignment

    def assignment(self):
        iden = self.current_token
        self.eat(types.IDENTIFIER)

        assign_token = self.current_token
        self.eat(types.ASSIGN)

        val = self.logical_or_expr()

        self.eat(types.SEMI_COLON)
        return AssignOp(left=iden, op=assign_token, right=val)  # Create an AST node for assignment

    def de_assignment(self):
        token = self.current_token
        self.eat(types.DELETE_VAR)

        iden = self.current_token
        self.eat(types.IDENTIFIER)
        self.eat(types.SEMI_COLON)
        return DeAssignOp(token=token, iden=iden)  # Create an AST node for assignment

    def print_STMT(self):
        statement = self.current_token
        self.eat(types.PRINT_STMT)
        self.eat(types.LPAREN)
        
        val = self.logical_or_expr()

        self.eat(types.RPAREN)
        self.eat(types.SEMI_COLON)

        return Print(statement, val)  # Create an AST node for assignment

    def handle_token(self):
        if self.current_token.type == types.SEMI_COLON:
            self.eat(types.SEMI_COLON)
            return None

        elif self.current_token.type in (types.INTEGER_TYPE, types.BOOL_TYPE, types.FLOAT_TYPE, types.STRING_TYPE):
            return self.declaration()

        elif self.current_token.type == types.DELETE_VAR:
            return self.de_assignment()

        elif self.current_token.type == types.PRINT_STMT:
            return self.print_STMT()

        elif self.current_token.type == types.IDENTIFIER and self.tokens[self.pos + 1].type == types.ASSIGN:
            return self.assignment()

        elif self.current_token.type == types.IF:
            return self.if_STMT()
        
        elif self.current_token.type == types.WHILE:
            return self.while_STMT()
        
        else:
            return self.logical_or_expr()  # Handle expressions

    def block(self):
        statements = []
        self.eat(types.CB_OPEN)  # Consume '{'

        while self.current_token.type != types.CB_CLOSE and self.current_token.type != types.EOF:
            stmt = self.handle_token()
            
            if stmt:
                statements.append(stmt)
        
        self.eat(types.CB_CLOSE)  # Consume '}'
        return statements
        
    def if_STMT(self):
        self.eat(types.IF)
        self.eat(types.LPAREN)

        node_val = self.logical_or_expr()
        
        self.eat(types.RPAREN)

        if self.current_token.type == types.CB_OPEN:
            body = self.block()  # Parse the block if { is found
        else:
            body = [self.handle_token()]  # Handle single statement

        return IfOp(expr=node_val, body=body)

    def while_STMT(self):
        self.eat(types.WHILE)
        self.eat(types.LPAREN)

        node_val = self.logical_or_expr()
        
        self.eat(types.RPAREN)

        if self.current_token.type == types.CB_OPEN:
            body = self.block()  # Parse the block if { is found
        else:
            body = [self.handle_token()]  # Handle single statement

        return WhileOp(expr=node_val, body=body)
    
    def factor(self):
        token = self.current_token

        if token.type == types.INTEGER:
            self.eat(types.INTEGER)
            return Num(token)
        
        elif token.type == types.STRING:
            self.eat(types.STRING)
            return String(token)
        
        elif token.type == types.FLOAT:
            self.eat(types.FLOAT)
            return Num(token)
        
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
        
        elif token.type == types.IDENTIFIER:
            return self.value()
        
        elif token.type == types.SEMI_COLON:
            self.eat(types.SEMI_COLON)
        
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
        while self.pos < len(self.tokens):
            if self.current_token.type == types.EOF:
                break

            stmt = self.handle_token()
            
            if stmt:
                self.AST_root.children.append(stmt)
            
        ast = [i for i in self.AST_root.children if i is not None]

        return ast