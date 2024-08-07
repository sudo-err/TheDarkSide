from sys import stdout, stderr
from requests import get

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


def decodeRawSource(url:str) -> list:
    ret_l = []
    table_lines = get(url).text.splitlines()[2:]
    for line in table_lines:
        tmp_l = line.split('|')
        name = tmp_l[1].strip()
        status = tmp_l[2].strip()
        if (status == "ONLINE"):
            link = name.split('(')[-1][:-1]
            ret_l.append(link)
    return ret_l

def downloadSources() -> list:
    ransom_url = "https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/ransomware_gang.md"
    markets_url = "https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/markets.md"
    forums_url = "https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/forum.md"

    ret_l = []

    #? Ransom decode
    pinfo("Downloading ransomware_gang.md")
    ret_l.extend(decodeRawSource(ransom_url))
    #? Markets decode
    pinfo("Downloading markets.md")
    ret_l.extend(decodeRawSource(markets_url))
    #? Forums decode
    pinfo("Downloading forum.md")
    ret_l.extend(decodeRawSource(forums_url))

    return list(set(ret_l))




def readUrlList(filepath:str) -> list:
    if (filepath == "DOWNLOAD"):
        return downloadSources()

    l = []
    with open(filepath, "r", encoding="utf-8") as in_f:
        l = [line.strip() for line in in_f.readlines() if (line.strip() != "")]
    for i in range(len(l)):
        if (not l[i].startswith("http://")):
            l[i] = "http://"+l[i]
        if (" (" in l[i]):
            l[i] = l[i].split(" ")[0]
    return list(set(l))
