from datatypes import *

class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        
        elif node.op.type == MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        
        elif node.op.type == DIVIDE:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        if node.op.type == MINUS:
            return -self.visit(node.expr)

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)