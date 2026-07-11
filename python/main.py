import sys
from scanning import Token, Scanner
from parsing.parser import Parser, Expr
from parsing.ast_printer import AstPrinter
from errors import ErrorReporter

import os

def run_file(file_path: str, reporter: ErrorReporter) -> None:
    file_str : str = ""
    with open(file_path, "r") as file:
        file_str = file.read()
    run(file_str, reporter)

def repl(reporter: ErrorReporter) -> None:
    try:
        while True:
            print("> ", end="")
            line = input()
            run(line, reporter)
            reporter.hadError = False
    except EOFError:
        print("\nExiting REPL")
    except KeyboardInterrupt:
        print("\nExiting REPL")

def run(source: str, reporter: ErrorReporter) -> None:
    if (reporter.hadError):
        exit(65) # data format error
    
    scanner: Scanner = Scanner(source, reporter)
    tokens: list[Token] = scanner.scanTokens()
    parser: Parser = Parser(tokens, reporter)
    expression: Expr | None = parser.parse()
    if expression is None:
        print("Aborted")
        return
    
    print(AstPrinter().print(expression))
    

def main() -> None:
    reporter: ErrorReporter = ErrorReporter()
    print("cwd:", os.getcwd())
    print("argv:", sys.argv)

    len_args : int = len(sys.argv)
    if len_args == 1:
        repl(reporter)
    elif len_args == 2:
        file_path : str = sys.argv[1]
        run_file(file_path, reporter)
    else:
        print("Usage: command <file_path>")
        exit(64)

if __name__ == "__main__":
    main()