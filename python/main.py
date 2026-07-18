import sys
from scanning import Token, Scanner
from parsing.parser import Parser, Expr
from parsing.stmt import Stmt, ExpressionStmt, PrintStmt
from parsing.ast_printer import AstPrinter
from errors import ErrorReporter
from interpret.interpreter import Interpreter
from interpret.environment import Environment

import os

def run_file(file_path: str, reporter: ErrorReporter) -> None:
    file_str : str = ""
    with open(file_path, "r") as file:
        file_str = file.read()
    run(file_str, reporter, Environment())

def repl(reporter: ErrorReporter) -> None:
    env: Environment = Environment()
    try:
        while True:
            print("> ", end="")
            line = input()
            env = run(line, reporter, env)
            reporter.hadError = False
    except EOFError:
        print("\nExiting REPL")
    except KeyboardInterrupt:
        print("\nExiting REPL")

def run(source: str, reporter: ErrorReporter, previous_env: Environment) -> Environment:
    if (reporter.hadError):
        exit(65) # data format error
    
    scanner: Scanner = Scanner(source, reporter)
    tokens: list[Token] = scanner.scanTokens()
    parser: Parser = Parser(tokens, reporter)
    program: list[Stmt] | None = parser.parse()
    if program is None:
        print("Aborted")
        return previous_env
    if len(program) > 0 and isinstance(program[-1], ExpressionStmt):
        stmt : ExpressionStmt = program[-1]
        program = program + [PrintStmt(stmt.expr)]
    interpreter: Interpreter = Interpreter(reporter, previous_env)
    interpreter.interpret(program)
    return interpreter.environment

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
    # main()
    run_file("../program.lox", ErrorReporter())