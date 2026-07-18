from parsing.expr import *
from parsing.stmt import *
from scanning import Token, TokenType
from typing import cast
from errors import ErrorReporter, LoxRuntimeError
from interpret.environment import Environment

class Interpreter(Expr.Visitor[object], Stmt.Visitor[None]):
    def __init__(self, reporter: ErrorReporter) -> None:
        self.reporter: ErrorReporter = reporter
        self.environment: Environment = Environment()

    def stringify(self, obj: object) -> str:
        if obj is None:
            return "Nil"
        return obj.__str__()


    def assertType(self, obj: object, expected: type, token: Token) -> None:
        try:
            assert isinstance(obj, expected)
        except AssertionError:
            raise LoxRuntimeError(token, f"[{token.line}] Runtime Error: At {token.lexeme}: Expected {expected.__name__}, but got {type(obj).__name__}")
        
    def interpret(self, statements: list[Stmt]) -> None:
        try:
            for stmt in statements:
                self.execute(stmt)
        except LoxRuntimeError as e:
            self.reporter.report(e.token.line, e.token.lexeme, e.__str__())

    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)
    
    def isTruthy(self, obj: object) -> bool:
        if obj == None:
            return False
        if isinstance(obj, bool):
            return obj
        return True
    
    def visitExpressionStmt(self, stmt: ExpressionStmt) -> None:
        self.evaluate(stmt.expr)
    
    def visitPrintStmt(self, stmt: PrintStmt) -> None:
        value: object = self.evaluate(stmt.expr)
        print(self.stringify(value))

    def visitLiteralExpr(self, expr: LiteralExpr) -> object:
            return expr.value
    
    def visitUnaryExpr(self, expr: UnaryExpr) -> object:
        ret: object = self.evaluate(expr.expr)

        match expr.token.type:
            case TokenType.MINUS:
                self.assertType(ret, float, expr.token)
                return -cast(float, ret)
            case TokenType.BANG:
                return not self.isTruthy(ret)
        # Unreachable
        return None

    def visitVarDeclStmt(self, stmt: VarDeclStmt) -> None:
        value: object = None
        if stmt.init is not None:
            value = self.evaluate(stmt.init)
        self.environment.define(stmt.name, value)

    def visitVarExpr(self, expr: VarExpr) -> object:
        return self.environment.get(expr.name)
    
    def visitAssignExpr(self, expr: AssignExpr) -> object:
        value: object = self.evaluate(expr.expr)
        self.environment.assign(expr.name, value)
        return value

    def visitBlockStmt(self, stmt: BlockStmt) -> None:
        # execute the current block
        fresh_environment: Environment = Environment(self.environment)
        self.executeBlock(stmt.statements, fresh_environment)

    def executeBlock(self, statements: list[Stmt], env: Environment) -> None:
        previous_environment: Environment = self.environment
        try:
            self.environment = env
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous_environment
    
    

    def visitBinaryExpr(self, expr: BinaryExpr) -> object:
        left_obj: object = self.evaluate(expr.left)
        right_obj: object = self.evaluate(expr.right)

        match expr.token.type:
            case TokenType.MINUS:
                self.assertType(left_obj, float, expr.token)
                self.assertType(right_obj, float, expr.token)
                return cast(float, left_obj) - cast(float, right_obj)
            case TokenType.SLASH:
                self.assertType(left_obj, float, expr.token)
                self.assertType(right_obj, float, expr.token)
                if cast(float, right_obj) == 0:
                    raise LoxRuntimeError(expr.token, f"[Line {expr.token.line}] Runtime Error: At {expr.token.lexeme}: Division by zero.")
                return cast(float, left_obj) / cast(float, right_obj)
            case TokenType.STAR:
                self.assertType(left_obj, float, expr.token)
                self.assertType(right_obj, float, expr.token)
                return cast(float, left_obj) * cast(float, right_obj)
            case TokenType.PLUS:
                if (isinstance(left_obj, float) and isinstance(right_obj, float)):
                    return left_obj + right_obj
                if (isinstance(left_obj, str) and isinstance(right_obj, str)):
                    return left_obj + right_obj
                if (isinstance(left_obj, str) and isinstance(right_obj, float)):
                    return left_obj + str(right_obj)
                if (isinstance(left_obj, float) and isinstance(right_obj, str)):
                    return str(left_obj) + right_obj
                token: Token = expr.token
                raise LoxRuntimeError(token, f"[Line {token.line}] Runtime Error: At {token.lexeme}: Operands must match (Numbers or Strings).")
            case TokenType.GREATER:
                self.assertType(left_obj, float, expr.token)
                self.assertType(right_obj, float, expr.token)
                return cast(float, left_obj) > cast(float, right_obj)
            case TokenType.GREATER_EQUAL:
                self.assertType(left_obj, float, expr.token)
                self.assertType(right_obj, float, expr.token)
                return cast(float, left_obj) >= cast(float, right_obj)
            case TokenType.LESS:
                self.assertType(left_obj, float, expr.token)
                self.assertType(right_obj, float, expr.token)
                return cast(float, left_obj) < cast(float, right_obj)
            case TokenType.LESS_EQUAL:
                self.assertType(left_obj, float, expr.token)
                self.assertType(right_obj, float, expr.token)
                return cast(float, left_obj) <= cast(float, right_obj)
            case TokenType.EQUAL_EQUAL:
                return left_obj == right_obj
            case TokenType.BANG_EQUAL:
                return not (left_obj == right_obj)

        return None
    
    def visitTernaryExpr(self, expr: TernaryExpr) -> object:
        raise LoxRuntimeError(expr.token, f"[Line {expr.token.line}] \"{expr.token.lexeme}\": Unsupported Operation.")
    def visitGroupingExpr(self, expr: GroupingExpr) -> object:
        return self.evaluate(expr.expr)
    def visitErrorExpr(self, expr: ErrorExpr) -> object:
        raise LoxRuntimeError(expr.token, f"[Line {expr.token.line}] \"{expr.token.lexeme}\": Unsupported Operation.")