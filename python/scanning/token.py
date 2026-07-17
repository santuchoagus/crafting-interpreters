from enum import StrEnum, auto

class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = object
        self.line = line
    
    def __str__(self) -> str:
        return f"({self.type} [{self.line}] {self.lexeme} {self.literal})"

class TokenType(StrEnum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    QUESTION = auto()
    COLON = auto()
    SEMICOLON = auto()
    BANG = auto()

    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    EQUAL = auto()

    SLASH = auto()
    STAR = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    VAR = auto()
    EOF = auto()

    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()

    PLUS = auto()
    MINUS = auto()
    
    AND = auto()
    OR = auto()
    IF = auto()
    ELSE = auto()
    CLASS = auto()
    TRUE = auto()
    FALSE = auto()
    NIL = auto()
    FOR = auto()
    PRINT = auto()
    RETURN = auto()
    THIS = auto()
    WHILE = auto()
    FUN = auto()