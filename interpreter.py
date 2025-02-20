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
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.op.type == PLUS:

            # If either operand is a string, perform string concatenation
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            
            return left + right  # Normal addition for numbers

        elif node.op.type == MINUS:
            return left - right

        elif node.op.type == MULTIPLY:
            return left * right

        elif node.op.type == DIVIDE:
            return left / right


    def visit_Num(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        if node.op.type == MINUS:
            return -self.visit(node.expr)

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)