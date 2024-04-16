from sys import stdout, stderr

def pinfo(msg:str) -> None:
    print(f"[INFO] {msg}", file=stdout)

def pwarning(msg:str) -> None:
    print(f"[WARN] {msg}", file=stdout)

def perror(msg:str) -> None:
    print(f"[ERROR] {msg}", file=stderr)

def appendOutput(out_path:str, append:str) -> None:
    with open(out_path,"a",encoding="utf-8") as out_f:
        out_f.write(append)
    return

def readUrlList(filepath:str) -> list:
    l = []
    with open(filepath, "r", encoding="utf-8") as in_f:
        l = [line for line in in_f.readlines() if (line != "")]
    for i in range(len(l)):
        if ("http" not in l[i]):
            l[i] = "http://"+l[i]
    return list(set(l))