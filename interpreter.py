from type import *

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.symbol_tree = [{}]
        self.skip_else = False

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
        return self.get_variable(node.name)

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

    def visit_DeclarationOp(self, node):
        value = self.visit(node.right)
        self.declare_variable(node.left.value, value)

    
    def visit_AssignOp(self, node):
        value = self.visit(node.right)
        self.set_variable(node.left.value, value)

    def visit_DeAssignOp(self, node):
        self.delete_variable(node.iden.value)

    def visit_IfOp(self, node):
        self.skip_else = False
        
        if self.visit(node.expr):
            self.symbol_tree.append({})  
            
            for stmt in node.body:
                self.visit(stmt)
                
            self.symbol_tree.pop()      
            self.skip_else = True


    def visit_ElseIfOp(self, node):
        if self.skip_else:
            return

        if self.visit(node.expr):
            self.symbol_tree.append({})  
            
            for stmt in node.body:
                self.visit(stmt)
            self.symbol_tree.pop()       
            self.skip_else = True

        
    def visit_ElseOp(self, node):
        if self.skip_else:
            return

        self.symbol_tree.append({})  
        for stmt in node.body:
            self.visit(stmt)
            
        self.symbol_tree.pop()       

        
    def visit_WhileOp(self, node):
        while self.visit(node.expr):
            self.symbol_tree.append({})  
            
            for stmt in node.body:
                self.visit(stmt)
            self.symbol_tree.pop()       


    def get_variable(self, name):
        for scope in reversed(self.symbol_tree):
            if name in scope:
                return scope[name]["value"]
            
        raise Exception(f"Variable '{name}' not found")

    def set_variable(self, name, value, expected_type=None):
        for scope in reversed(self.symbol_tree):
            if name in scope:
                if expected_type and type(value) != expected_type:
                    raise Exception(f"Type mismatch for variable '{name}'")
                
                scope[name]["value"] = value
                return
            
        raise Exception(f"Variable '{name}' not found")

    def declare_variable(self, name, value):
        current_scope = self.symbol_tree[-1]
        
        if name in current_scope:
            raise Exception(f"Variable '{name}' already declared in current scope")
        
        current_scope[name] = {"type": type(value), "value": value}

    def delete_variable(self, name):
        for scope in reversed(self.symbol_tree):
            if name in scope:
                del scope[name]
                return
            
        raise Exception(f"Variable '{name}' not found to delete")

    def interpret(self):
        for node in self.tree:
            self.visit(node)
            
            
            