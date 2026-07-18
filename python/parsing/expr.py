from scanning import Token
from typing import Protocol, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass
from parsing.r_typevar import R

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
        def visitVarExpr(self, expr: VarExpr) -> R: ...
        def visitErrorExpr(self, expr: ErrorExpr) -> R: ...
        def visitAssignExpr(self, expr: AssignExpr) -> R: ...
        def visitLogicalExpr(self, expr: LogicalExpr) -> R: ...


@dataclass
class ErrorExpr(Expr):
    token: Token
    def accept(self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visitErrorExpr(self)

@dataclass
class LiteralExpr(Expr):
    value: object
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

@dataclass
class VarExpr(Expr):
    name: Token
    def accept(self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visitVarExpr(self)
    
@dataclass 
class AssignExpr(Expr):
    name: Token
    expr: Expr
    def accept(self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visitAssignExpr(self)

    
@dataclass 
class LogicalExpr(Expr):
    operator: Token
    left: Expr
    right: Expr
    def accept(self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visitLogicalExpr(self)


