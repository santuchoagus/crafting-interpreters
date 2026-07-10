hadError : bool = False
def report(line : int, where : str, message : str) -> None:
    print(f"[Line {line}] Error {where}: \"{message}\"")
    hadError = True
    
def error(line : int, message : str) -> None:
    report(line, "", message)