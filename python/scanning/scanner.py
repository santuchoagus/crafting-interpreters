from errors import ErrorReporter
from scanning import Token, TokenType

class Scanner:
    def __init__(self, source: str, reporter: ErrorReporter):
        self.source: str = source
        self.tokens: list[Token] = list()
        self.line: int = 1
        self.reporter: ErrorReporter = reporter

    def addToken(self, token: Token) -> None:
        self.tokens.append(token)


    def peek(self, i: int) -> str | None:
        if i >= len(self.source):
            return None
        return self.source[i]

    def matchAt(self, i: int, char: str) -> bool:
        if i >= len(self.source) or self.source[i] != char:
            return False
        return True
    
    def scanTokens(self) -> list[Token]:
        self.line = 1
        self.tokens.clear()

        shouldSkip: bool = False
        insideComment: bool = False
        insideString: bool = False
        insideNumber: bool = False
        insideIdentifier: bool = False
        decimalDotWasVisited: bool = False

        scanRange: tuple[int, int] = (0,0)
        for i, c in enumerate(self.source):
            if insideComment and c != "\n":
                continue
            insideComment = False

            if insideString and c != "\"":
                if c == "\n":
                    self.line += 1
                continue
            else:
                scanRange = (scanRange[0], i)
            
            #not inside string
            if c.isalpha() or c=="_":
                if not insideIdentifier:
                    scanRange = (i, scanRange[1])
                insideIdentifier = True
            elif insideIdentifier:
                nextChar: str | None = self.peek(i+1) 
                if (not nextChar) or not (c.isalpha() or c=="_" or c.isdigit()):
                    insideIdentifier = False
                    scanRange = (scanRange[0], i)
                    identifier: str = self.source[scanRange[0]:scanRange[1]]
                    if identifier in KeywordMap.keys():
                        self.addToken(Token(KeywordMap[identifier], identifier, None, self.line))
                    else:
                        self.addToken(Token(TokenType.IDENTIFIER, identifier, None, self.line))
                    
            if insideIdentifier:
                if self.peek(i+1) is None:
                    scanRange = (scanRange[0], i+1)
                    identifier = self.source[scanRange[0]:scanRange[1]]
                    if identifier in KeywordMap.keys():
                        self.addToken(Token(KeywordMap[identifier], identifier, None, self.line))
                    else:
                        self.addToken(Token(TokenType.IDENTIFIER, identifier, None, self.line))
                continue

            if shouldSkip:
                shouldSkip = False
                continue

            if c.isdigit():
                if not insideNumber:
                    scanRange = (i, scanRange[1])
                insideNumber = True
            elif insideNumber:
                nextChar = self.peek(i+1)
                if c == ".":
                    if not nextChar or not nextChar.isdigit():
                        self.reporter.report(self.line, self.source[scanRange[0]:i+1], "Number shouldn't end with a decimal dot.") 
                    if decimalDotWasVisited:
                        self.reporter.report(self.line, self.source[scanRange[0]:i+1], "Multiple dots in decimal definition.")
                    decimalDotWasVisited = True
                else:
                    insideNumber = False
                    scanRange = (scanRange[0], i)
                    self.addToken(Token(TokenType.NUMBER, self.source[scanRange[0]:scanRange[1]], None, self.line))
            
            if insideNumber:
                if self.peek(i+1) is None:
                    scanRange = (scanRange[0], i+1)
                    self.addToken(Token(TokenType.NUMBER, self.source[scanRange[0]:scanRange[1]], None, self.line))
                continue
            decimalDotWasVisited = False

            match c:
                case "\n":
                    self.line += 1
                    insideComment = False
                case " " | "\r" | "\t":
                    pass
                case "(":
                    self.addToken(Token(TokenType.LEFT_PAREN, c, None, self.line))
                case ")":
                    self.addToken(Token(TokenType.RIGHT_PAREN, c, None, self.line))
                case "{":
                    self.addToken(Token(TokenType.LEFT_BRACE, c, None, self.line))
                case "}":
                    self.addToken(Token(TokenType.RIGHT_BRACE, c, None, self.line))
                case ",":
                    self.addToken(Token(TokenType.COMMA, c, None, self.line))
                case ";":
                    self.addToken(Token(TokenType.SEMICOLON, c, None, self.line))
                case "+":
                    self.addToken(Token(TokenType.PLUS, c, None, self.line))
                case "-":
                    self.addToken(Token(TokenType.MINUS, c, None, self.line))
                case "*":
                    self.addToken(Token(TokenType.STAR, c, None, self.line))
                case "?":
                    self.addToken(Token(TokenType.QUESTION, c, None, self.line))
                case ":":
                    self.addToken(Token(TokenType.COLON, c, None, self.line))
                case "=":
                    if self.matchAt(i+1, "="):
                        self.addToken(Token(TokenType.EQUAL_EQUAL, "==", None, self.line))
                        shouldSkip = True
                    else:
                        self.addToken(Token(TokenType.EQUAL, c, None, self.line))
                case "!":
                    if self.matchAt(i+1, "="):
                        self.addToken(Token(TokenType.BANG_EQUAL, "!=", None, self.line))
                        shouldSkip = True
                    else:
                        self.addToken(Token(TokenType.BANG, c, None, self.line))
                case "/":
                    if self.matchAt(i+1, "/"):
                        insideComment = True
                    else:
                        self.addToken(Token(TokenType.SLASH, c, None, self.line))
                case "\"":
                    if not insideString:
                        scanRange = (i+1, scanRange[1])
                        insideString = True
                        continue
                    insideString = False
                    str_literal: str = self.source[scanRange[0]:scanRange[1]]
                    self.addToken(Token(TokenType.STRING, str_literal, None, self.line))
                    
                case _:
                    self.reporter.report(self.line, c, "Unrecognized token.")
        ...

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens.copy()

KeywordMap = {
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "print": TokenType.PRINT,
    "var": TokenType.VAR,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "and": TokenType.AND,
    "or": TokenType.OR
}