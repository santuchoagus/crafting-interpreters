import time
from typing import Protocol, TYPE_CHECKING
from abc import ABC, abstractmethod
from parsing.stmt import Stmt, FunDeclStmt
from interpret.environment import Environment, Return

if TYPE_CHECKING:
    from interpret.interpreter import Interpreter

class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int: ...
    @abstractmethod
    def call(self, interpreter: Interpreter, arguments: list[object]) -> object: ...

class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunDeclStmt, closure: Environment) -> None:
        self.closure = closure
        self.declaration = declaration
    def call(self, interpreter: Interpreter, arguments: list[object]) -> object:
        environment: Environment = Environment(self.closure)

        for i, arg in enumerate(arguments):
            environment.define(self.declaration.parameters[i], arg)
        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except Return as e:
            return e.value
        except Exception as e:
            interpreter.reporter.error(self.declaration.name, e)
        return None
    
    def arity(self) -> int:
        return len(self.declaration.parameters)
    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme} {self.arity()}>"

class clockCallable(LoxCallable):
    def arity(self) -> int:
        return 0
    def call(self, interpreter: Interpreter, arguments: list[object]) -> object:
        return time.time()
    def __str__(self) -> str:
        return "<native loxCallable>"
