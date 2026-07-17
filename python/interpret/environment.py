from errors import LoxRuntimeError
from scanning import Token

class Environment:
    def __init__(self) -> None:
        self.values : dict[str, object] = dict()
    
    def define(self, name: Token, value: object) -> None:
        self.values[name.lexeme] = value

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme not in self.values.keys():
            raise LoxRuntimeError(name, f"[Line {name.line}] Error: Undefined variable \"{name.lexeme}\".")
        self.values[name.lexeme] = value

    def get(self, name: Token) -> object:
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme] 
        raise LoxRuntimeError(name, f"[Line {name.line}] Error: Undefined variable \"{name.lexeme}\".")