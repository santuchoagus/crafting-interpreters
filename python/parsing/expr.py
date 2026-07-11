from scanning import Token
from typing import Literal, Protocol, TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass

R = TypeVar("R", covariant=True)
# Visitor pattern to define operations
class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor[R]) -> R: ...

    class Visitor(Protocol, Generic[R]):
        def visitLiteralExpr(self, expr: LiteralExpr) -> R: ...
        def visitUnaryExpr(self, expr: UnaryExpr) -> R: ...
        def visitBinaryExpr(self, expr: BinaryExpr) -> R: ...
        def visitTernaryExpr(self, expr: TernaryExpr) -> R: ...
        def visitGroupingExpr(self, expr: GroupingExpr) -> R: ...
        def visitErrorExpr(self, expr: ErrorExpr) -> R: ...


@dataclass
class ErrorExpr(Expr):
    def accept(self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visitErrorExpr(self)

class LiteralObject(ABC):
    def __str__(self) -> str:
        return "<object>"

@dataclass
class LiteralNumber(LiteralObject):
    value: float
    def __str__(self) -> str:
        return self.value.__str__()
    
@dataclass
class LiteralString(LiteralObject):
    value: str
    def __str__(self) -> str:
        return f"\"{self.value}\""

@dataclass
class LiteralTrue(LiteralObject):
    def __str__(self) -> str:
        return "True"

@dataclass
class LiteralFalse(LiteralObject):
    def __str__(self) -> str:
        return "False"


@dataclass
class LiteralNil(LiteralObject):
    def __str__(self) -> str:
        return "Nil"

@dataclass
class LiteralExpr(Expr):
    value: LiteralObject
    def accept(self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visitLiteralExpr(self)

@dataclass
class UnaryExpr(Expr):
    token: Token
    expr: Expr
    def accept(self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visitUnaryExpr(self)

@dataclass
class BinaryExpr(Expr):
    token: Token
    left: Expr
    right: Expr
    def accept(self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visitBinaryExpr(self)

@dataclass
class TernaryExpr(Expr):
    token: Token
    left: Expr
    middle: Expr
    right: Expr
    def accept(self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visitTernaryExpr(self)
    

@dataclass
class GroupingExpr(Expr):
    expr: Expr
    def accept(self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visitGroupingExpr(self)



