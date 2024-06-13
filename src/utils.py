from sys import stdout, stderr

def pinfo(msg:str, end:str="\n") -> None:
    print(f"[INFO] {msg}", end=end, file=stdout)

def pwarning(msg:str, end:str="\n") -> None:
    print(f"[WARN] {msg}", end=end, file=stdout)

def perror(msg:str, end:str="\n") -> None:
    print(f"[ERROR] {msg}", end=end, file=stderr)

def appendOutput(out_path:str, append:str) -> None:
    with open(out_path,"a",encoding="utf-8") as out_f:
        out_f.write(append)
    return

def readUrlList(filepath:str) -> list:
    l = []
    with open(filepath, "r", encoding="utf-8") as in_f:
        l = [line.strip() for line in in_f.readlines() if (line.strip() != "")]
    for i in range(len(l)):
        if (not l[i].startswith("http://")):
            l[i] = "http://"+l[i]
        if (" (" in l[i]):
            l[i] = l[i].split(" ")[0]
    return list(set(l))
