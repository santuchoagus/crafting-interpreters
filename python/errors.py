class ErrorReporter:
    def __init__(self) -> None:
        self.hadError: bool = False

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[Line {line}] Error at \"{where}\": {message}")

class ParseError(Exception):
    pass