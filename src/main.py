from Scraper import Scraper
from Crawler import Crawler
from utils import *

from typing import Any, Dict
from argparse import ArgumentParser
from os import getcwd

NAME = "TheDarkSide"

# ----------------------------------------------------------


def parseArgs() -> Dict[str,Any]:
    arg_d = {

    }
    ap = ArgumentParser()
    ap.description = f"{NAME} - Dark web scraper and crawler"
    
    return arg_d



def buildOutPath() -> str:
    cwd = getcwd()
    if ("TheDarkSide" not in cwd):
        perror(f"Not working from a standard directory ({NAME} expected), aborting")
        exit(1)
    out_path = ""
    for d in cwd.split("/"):
        if d == "": continue
        out_path += ("/"+d)
        if d == NAME:
            out_path += "/out"
            break
    return out_path



def main() -> None:
    out_path = buildOutPath()
    args = parseArgs()

    print(out_path)
    
    return









# ----------------------------------------------------------

if (__name__ == "__main__"):
    main()