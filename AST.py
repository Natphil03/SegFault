class AST:
    def __init__(self):
        self.children = []

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
        
class IfOp(AST):
    def __init__(self, expr, body):
        self.expr = expr
        self.body = body
        
class Identifier(AST):
    def __init__(self, token):
        self.token = token
        self.name = token.value  

class DeclarationOp(AST):
    def __init__(self, type, left, op, right):
        self.type = type
        self.left = left  # Identifier node (variable name)
        self.token = self.op = op  # Assignment token '='
        self.right = right  # Expression on the right-hand side
    
class AssignOp(AST):
    def __init__(self, left, op, right):
        self.left = left  # Identifier node (variable name)
        self.token = self.op = op  # Assignment token '='
        self.right = right  # Expression on the right-hand side
        
class DeAssignOp(AST):
    def __init__(self, token, iden):
        self.token = token
        self.iden = iden
      
class Print(AST):
    def __init__(self, token, value):
        self.token = token
        self.value = value