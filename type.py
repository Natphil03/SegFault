from enum import Enum

class types(Enum):
    INTEGER = 1,
    BOOL = 2,
    STRING = 3,
    PLUS = 4,
    MINUS = 5,
    MULTIPLY = 6,
    DIVIDE = 7,
    LPAREN = 8,
    RPAREN = 9,
    EOF = 10,
    NEGATE = 11,
    EQUAL = 12,
    NOTEQUAL = 13,
    GREATERTHAN = 14,
    LESSTHAN = 15,
    GREATERTHAN_EQUAL = 16,
    LESSTHAN_EQUAL = 17,
    FALSE = 18,
    TRUE = 19,
    NOT = 20,
    AND = 21,
    OR = 22,
    
    