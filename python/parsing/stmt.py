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
        def visitIfStmt(self, stmt: IfStmt) -> R: ...
        def visitWhileStmt(self, stmt: WhileStmt) -> R: ...
        def visitForStmt(self, stmt: ForStmt) -> R: ...


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
    
@dataclass
class IfStmt(Stmt):
    condition: Expr
    then_stmt: Stmt
    else_stmt: Stmt | None
    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visitIfStmt(self)

@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: Stmt
    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visitWhileStmt(self)

@dataclass
class ForStmt(Stmt):
    initializer: VarDeclStmt | ExpressionStmt | None
    condition: Expr | None
    increment: Expr | None
    body: Stmt
    def accept(self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visitForStmt(self)