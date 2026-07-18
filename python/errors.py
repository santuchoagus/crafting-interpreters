from parsing.expr import Expr
from scanning import Token

class ErrorReporter:
    def __init__(self) -> None:
        self.hadError: bool = False

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[Line {line}] Error at \"{where}\": {message}")

class LoxRuntimeError(Exception):
    def __init__(self, token: Token | None, message: str):
        super().__init__(message)
        if token is not None:
            self.token: Token = token

class ParseError(Exception):
    def __init__(self, token: Token | None, message: str):
        super().__init__(message)
        if token is not None:
            self.token: Token = token