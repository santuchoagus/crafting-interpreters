import sys
from scanning import Token, Scanner
from errors import hadError
import os

def run_file(file_path : str) -> None:
    file_str : str = ""
    with open(file_path, "r") as file:
        file_str = file.read()
    run(file_str)

def repl() -> None:
    try:
        while True:
            print("> ", end="")
            line = input()
            run(line)
            hadError = False
    except EOFError:
        print("\nExiting REPL")
    except KeyboardInterrupt:
        print("\nExiting REPL")

def run(source : str) -> None:
    if (hadError):
        exit(65) # data format error
    
    scanner : Scanner = Scanner(source)
    
    for token in scanner.scanTokens():
        print(token)

def main() -> None:
    print("cwd:", os.getcwd())
    print("argv:", sys.argv)

    len_args : int = len(sys.argv)
    if len_args == 1:
        repl()
    elif len_args == 2:
        file_path : str = sys.argv[1]
        run_file(file_path)
    else:
        print("Usage: command <file_path>")
        exit(64)



from parsing.expr import *
from parsing.ast_printer import AstPrinter
from scanning.scanner import TokenType
def foo() ->  None:
    # expression = BinaryExpr(
    #         Token(TokenType.STAR, "*", None, 1),
    #         UnaryExpr(Token(TokenType.MINUS, "-", None, 1), LiteralNumber(203.3)),
    #         GroupingExpr(LiteralNil())
    #     )
    # print(expression.accept(AstPrinter))
    expression = UnaryExpr(
        Token(TokenType.STAR, "*", None, 1),
        BinaryExpr(
            Token(TokenType.AND, "&", None, 1),
            LiteralExpr(LiteralNil()),
            GroupingExpr(LiteralExpr(LiteralString("Hello this is a string")))
        )
    )

    print(AstPrinter().print(expression))

if __name__ == "__main__":
    foo()