from type import *

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.symbol_tree = {}

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'

        if method_name == 'visit_NoneType':
            return

        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_BoolOp(self, node):
        if node.op.type == types.TRUE:
            return True
        
        if node.op.type == types.FALSE:
            return False

        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.op.type == types.EQUAL:
            return left == right
        
        elif node.op.type == types.NOTEQUAL:
            return left != right
        
        elif node.op.type == types.GREATERTHAN:
            return left > right
        
        elif node.op.type == types.LESSTHAN:
            return left < right
        
        elif node.op.type == types.GREATERTHAN_EQUAL:
            return left >= right
        
        elif node.op.type == types.LESSTHAN_EQUAL:
            return left <= right
        
        elif node.op.type == types.AND:
            return left and right

        elif node.op.type == types.OR:
            return left or right
    
    def visit_Identifier(self, node):
        if node.name in self.symbol_tree:
            return self.symbol_tree[node.name]
        else:
            return Exception("Variable does not exist")


    def visit_BinOp(self, node):

        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == types.PLUS:

            # If either operand is a string, perform string concatenation
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            
            return left + right  # Normal addition for numbers

        elif node.op.type == types.MINUS:
            return left - right

        elif node.op.type == types.MULTIPLY:
            return left * right

        elif node.op.type == types.DIVIDE:
            return left / right

    def visit_Num(self, node):
        if node.token.type == types.INTEGER:
            return int(node.value) 
        elif node.token.type == types.FLOAT:
            return float(node.value)

    def visit_Print(self, node):
        print(self.visit(node.value))

    def visit_String(self, node):
        if node.token.type == types.STRING:
            return str(node.value)

    def visit_UnaryOp(self, node):
        if node.op.type == types.MINUS:
            return -self.visit(node.expr)
        
        if node.op.type == types.NOT:
            return not self.visit(node.expr)

    def visit_AssignOp(self, node):
        self.symbol_tree[node.left.value] = self.visit(node.right)

    def visit_DeAssignOp(self, node):
        if node.iden.value in self.symbol_tree:
            self.symbol_tree.pop(node.iden.value)
        else:
            return Exception("Variable does not exist")

    def interpret(self):
        for node in self.tree:
            result = self.visit(node)

            # if(result is not None):
            #    print(result) 