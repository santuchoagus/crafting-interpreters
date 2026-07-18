from scanning import Token, TokenType
from parsing.expr import *
from parsing.stmt import *
from errors import ErrorReporter, ParseError

class Parser:
    def __init__(self, tokens: list[Token], reporter: ErrorReporter):
        self.tokens: list[Token] = tokens
        self.curr_index: int = 0 
        self.reporter: ErrorReporter = reporter
        self.statements: list[Stmt] = list()

    def parse(self) -> None | list[Stmt]:
        try:
            # return self.expression()
            while (self.curr_index < len(self.tokens)):
                if self.tokens[self.curr_index].type == TokenType.EOF:
                    break
                self.statements.append(self.declaration())
        except ParseError as e:
            self.reporter.report(e.token.line, e.token.lexeme, e.__str__())
            return None
        return self.statements

    
    # helpers
    def peek(self) -> Token | None:
        if (self.curr_index >= len(self.tokens)):
            return None
        
        return self.tokens[self.curr_index]
    
    def advance(self) -> None:
        self.curr_index += 1

    def match(self, *types: TokenType) -> Token | None:
        token: Token | None = self.peek() 
        if token and token.type in types:
            self.curr_index += 1
            return token
        else:
            return None
    
    def consume(self, *types: TokenType, error_message: str) -> None:
        token: Token | None = self.match(*types)
        if token is None or token.type not in types:
            raise ParseError(self.peek(), f"{error_message}")

    # grammar
    def declaration(self) -> Stmt:
        if (token := self.peek()) is not None and token.type is TokenType.VAR:
            return self.varDeclaration()
        else:
            return self.statement()

    def varDeclaration(self) -> Stmt:
        self.consume(TokenType.VAR, error_message="")
        identifier: Token | None = self.match(TokenType.IDENTIFIER)
        if identifier is None:
            raise ParseError(self.peek(), f"Expected variable name.")
        
        initializer: Expr | None = None
        if (token := self.match(TokenType.EQUAL)) is not None:
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, error_message="Expected \";\" after variable declaration.")
        return VarDeclStmt(identifier, initializer)

    def statement(self) -> Stmt:
        if (token := self.peek()) is not None and token.type is TokenType.PRINT:
            self.consume(TokenType.PRINT, error_message="")
            return self.printStatement()
        elif (token := self.peek()) is not None and token.type is TokenType.LEFT_BRACE:
            return self.blockStatement()
        elif (token := self.peek()) is not None:
            return self.expressionStatement()
        raise Exception("Unreachable")
    
    def blockStatement(self) -> Stmt:
        self.consume(TokenType.LEFT_BRACE, error_message="")
        statements: list[Stmt] = list()

        while (token := self.peek()) is not None:
            t: TokenType = token.type
            if t is TokenType.RIGHT_BRACE or t is TokenType.EOF:
                break
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, error_message="Expected \"}\" after block.")
        return BlockStmt(statements)

    def printStatement(self) -> Stmt:
        expr: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, error_message="Expected \";\" after value.")
        return PrintStmt(expr)

    def expressionStatement(self) -> Stmt:
        expr: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, error_message="Expected \";\" after expression.")
        return ExpressionStmt(expr)

    def expression(self) -> Expr:
        return self.comma()

    def comma(self) -> Expr:
        # error handling
        if (token := self.peek()) is not None and token.type is TokenType.COMMA:
            self.reporter.report(token.line, token.lexeme,  "Missing , left hand operand.")
            self.consume(TokenType.COMMA, error_message="")
            self.conditional() # discarding this conditional
            return ErrorExpr(token)

        expr: Expr = self.assignment() #rec. des.
        while (token := self.match(TokenType.COMMA)) is not None:
            right_expr: Expr = self.assignment() #rec. des.
            expr = BinaryExpr(token, expr, right_expr)
        return expr
    
    def assignment(self) -> Expr:
        expr: Expr = self.equality()
        token: Token | None = self.match(TokenType.EQUAL)
        if token is not None:
            value: Expr = self.assignment()
            if isinstance(expr, VarExpr):
                return AssignExpr(expr.name, value)
            raise ParseError(token, f"Invalid assignment target.")
        return expr
        
    # I can do right recursion here because I already consumed the left tokens
    # conditional -> equality ("?" expression ":" conditional)?
    def conditional(self) -> Expr:
        expr: Expr = self.equality()
        if (token := self.match(TokenType.QUESTION)) is not None:
            middle_expr: Expr = self.expression()
            if self.match(TokenType.COLON) is not None:
                right_expr: Expr = self.conditional()
                expr = TernaryExpr(token, expr, middle_expr, right_expr)
        return expr
    
    def equality(self) -> Expr:
        expr: Expr = self.comparision() #rec. des.
        while (token := self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL)) is not None:
            right_expr: Expr = self.comparision() #rec. des.
            expr = BinaryExpr(token, expr, right_expr)
        return expr

    def comparision(self) -> Expr:
        expr: Expr = self.term()
        while (token := self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)) is not None:
            right_expr: Expr = self.term() #rec. des.
            expr = BinaryExpr(token, expr, right_expr)
        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor() #rec. des.
        while (token := self.match(TokenType.MINUS, TokenType.PLUS)) is not None:
            right_expr: Expr = self.factor() #rec. des.
            expr = BinaryExpr(token, expr, right_expr)
        return expr
    
    def factor(self) -> Expr:
        expr: Expr = self.unary() #rec. des.
        while (token := self.match(TokenType.SLASH, TokenType.STAR)) is not None:
            right_expr: Expr = self.unary() #rec. des.
            expr = BinaryExpr(token, expr, right_expr)
        return expr
    
    def unary(self) -> Expr:
        if (token := self.match(TokenType.BANG, TokenType.MINUS)) is not None:
            inner_expr: Expr = self.primary() #rec. des.
            return UnaryExpr(token, inner_expr)
        return self.primary()
        
    def primary(self) -> Expr:
        if (token := self.match(TokenType.FALSE)) is not None:
            return LiteralExpr(False)
        if (token := self.match(TokenType.TRUE)) is not None:
            return LiteralExpr(True)
        if (token := self.match(TokenType.NIL)) is not None:
            return LiteralExpr(None)
        if (token := self.match(TokenType.NUMBER)) is not None:
            return LiteralExpr(float(token.lexeme))
        if (token := self.match(TokenType.STRING)) is not None:
            return LiteralExpr(token.lexeme)
        if (token := self.match(TokenType.LEFT_PAREN)) is not None:
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, error_message="Expected ).")
            return GroupingExpr(expr)
        if (token := self.match(TokenType.IDENTIFIER)) is not None:
            return VarExpr(token)
        
        if (token := self.peek()) is not None:
            self.reporter.report(token.line, token.lexeme, "Expected expression.")
        raise ParseError(self.peek(), "Expected expression, unrecoverable error.")
    
    def synchronize(self) -> None:
        self.curr_index += 1

        while (token := self.peek()) is not None:
            if (token.type == TokenType.SEMICOLON):
                return
            self.curr_index += 1


