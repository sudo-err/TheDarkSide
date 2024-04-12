from sys import stdout, stderr

def pinfo(msg:str) -> None:
    print(f"[INFO] {msg}", file=stdout)

def pwarning(msg:str) -> None:
    print(f"[WARN] {msg}", file=stdout)

def perror(msg:str) -> None:
    print(f"[ERROR] {msg}", file=stderr)