from scanning import Token, TokenType
from parsing.expr import *
from errors import ErrorReporter, ParseError

class Parser:
    def __init__(self, tokens: list[Token], reporter: ErrorReporter):
        self.tokens: list[Token] = tokens
        self.curr_index: int = 0 
        self.reporter: ErrorReporter = reporter

    def parse(self) -> Expr | None:
        try:
            return self.expression()
        except Exception as e:
            return None

    
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
            raise ParseError(f"{error_message}")

    # grammar
    def expression(self) -> Expr:
        return self.comma()

    def comma(self) -> Expr:
        # error handling
        if (token := self.peek()) is not None and token.type is TokenType.COMMA:
            self.reporter.report(token.line, token.lexeme,  "Missing , left hand operand.")
            self.consume(TokenType.COMMA, error_message="")
            self.conditional() # discarding this conditional
            return ErrorExpr()

        expr: Expr = self.conditional() #rec. des.
        while (token := self.match(TokenType.COMMA)) is not None:
            right_expr: Expr = self.conditional() #rec. des.
            expr = BinaryExpr(token, expr, right_expr)
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
        if (token := self.match(TokenType.BANG, TokenType.BANG_EQUAL)) is not None:
            inner_expr: Expr = self.primary() #rec. des.
            return UnaryExpr(token, inner_expr)
        return self.primary()
        
    def primary(self) -> Expr:
        if (token := self.match(TokenType.FALSE)) is not None:
            return LiteralExpr(LiteralFalse())
        if (token := self.match(TokenType.TRUE)) is not None:
            return LiteralExpr(LiteralTrue())
        if (token := self.match(TokenType.NIL)) is not None:
            return LiteralExpr(LiteralNil())
        if (token := self.match(TokenType.NUMBER)) is not None:
            return LiteralExpr(LiteralNumber(float(token.lexeme)))
        if (token := self.match(TokenType.STRING)) is not None:
            return LiteralExpr(LiteralString(token.lexeme))
        if (token := self.match(TokenType.LEFT_PAREN)) is not None:
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, error_message="Expected ).")
            return GroupingExpr(expr)
        
        if (token := self.peek()) is not None:
            self.reporter.report(token.line, token.lexeme, "Expected expression.")
        raise ParseError("Expected expression, unrecoverable error.")
    
    def synchronize(self) -> None:
        self.curr_index += 1

        while (token := self.peek()) is not None:
            if (token.type == TokenType.SEMICOLON):
                return
            self.curr_index += 1


