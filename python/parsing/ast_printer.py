from parsing.expr import *

class AstPrinter(Expr.Visitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)
    def visitUnaryExpr(self, expr: UnaryExpr) -> str:
        return f"({expr.token.lexeme} {expr.expr.accept(self)})"
    def visitBinaryExpr(self, expr: BinaryExpr) -> str:
        return f"({expr.token.lexeme} {expr.left.accept(self)} {expr.right.accept(self)})"
    def visitTernaryExpr(self, expr: TernaryExpr) -> str:
        return f"({expr.token.lexeme} {expr.left.accept(self)} {expr.middle.accept(self)} {expr.right.accept(self)})"
    def visitGroupingExpr(self, expr: GroupingExpr) -> str:
        return f"(group {expr.expr.accept(self)})"
    def visitLiteralExpr(self, expr: LiteralExpr) -> str:
        return expr.value.__str__()
    def visitErrorExpr(self, _: ErrorExpr) -> str:
        return ""