from enum import Enum

class types(Enum):
    
    # Types
    INTEGER = 1,
    BOOL = 2,
    STRING = 3,
    FLOAT = 28,
    
    # Variable Declaration Types
    INTEGER_TYPE = 25,
    STRING_TYPE = 29,
    FLOAT_TYPE = 31,
    BOOL_TYPE = 32,
    
    # Boolean
    FALSE = 18,
    TRUE = 19,
    NOT = 20,
    AND = 21,
    OR = 22,
    
    # Boolean Operations
    NEGATE = 11,
    EQUAL = 12,
    NOTEQUAL = 13,
    GREATERTHAN = 14,
    LESSTHAN = 15,
    GREATERTHAN_EQUAL = 16,
    LESSTHAN_EQUAL = 17,
    
    # Assignment and Declaration
    ASSIGN = 23,
    DECLARATION = 27,
    
    # Operations
    PLUS = 4,
    MINUS = 5,
    MULTIPLY = 6,
    DIVIDE = 7,
    
    # Statements
    PRINT_STMT = 30,
    DELETE_VAR = 33,
    
    # Control Flow
    IF = 40,
    WHILE = 41,
    FOR = 42,
    
        
    LPAREN = 8,
    RPAREN = 9,
    SEMI_COLON = 26,
    CB_OPEN = 43,
    CB_CLOSE = 44,
    IDENTIFIER = 24,
    EOF = 10,
    
operators = ("+", "-", "/", "*")
