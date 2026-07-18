from scanning import Token
from typing import Protocol, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass
from parsing.expr import Expr
from parsing.r_typevar import R

# Visitor pattern to define operations
class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor[R]) -> R: ...

    class Visitor(Protocol, Generic[R]):
        def visitExpressionStmt(self, stmt: ExpressionStmt) -> R: ...
        def visitVarDeclStmt(self, stmt: VarDeclStmt) -> R: ...
        def visitPrintStmt(self, stmt: PrintStmt) -> R: ...
        def visitBlockStmt(self, stmt: BlockStmt) -> R: ...


@dataclass
class ExpressionStmt(Stmt):
    expr: Expr
    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visitExpressionStmt(self)
    
@dataclass
class VarDeclStmt(Stmt):
    name: Token
    init: Expr | None
    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visitVarDeclStmt(self)
    
@dataclass
class PrintStmt(Stmt):
    expr: Expr
    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visitPrintStmt(self)
    
@dataclass
class BlockStmt(Stmt):
    statements: list[Stmt]
    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visitBlockStmt(self)