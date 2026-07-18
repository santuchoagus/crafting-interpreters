from errors import LoxRuntimeError
from scanning import Token

class Environment:
    def __init__(self, parent: Environment | None = None) -> None:
        self.parent: Environment | None = parent 
        self.values: dict[str, object] = dict()

    def define(self, name: Token, value: object) -> None:
        self.values[name.lexeme] = value

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
            return
        if self.parent is not None:
            self.parent.assign(name, value)
        else:
            raise LoxRuntimeError(name, f"[Line {name.line}] Error: Undefined variable \"{name.lexeme}\".")

    def get(self, name: Token) -> object:
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        if self.parent is not None:
            return self.parent.get(name)
        raise LoxRuntimeError(name, f"[Line {name.line}] Error: Undefined variable \"{name.lexeme}\".")