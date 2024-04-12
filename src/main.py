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
        "mode": None,       #? scrape / crawl (str)
        "depth": None,      #? if crawl, depth to go from start (int)
        "url_list": None,   #? if scrape, the list of input urls (file)
        "search": None,     #? if scrape, the term(s) to search for (str)
        "out": None,        #? the output file name (will always be in /out)      
    }
    ap = ArgumentParser()
    ap.description = f"{NAME} - Dark web scraper and crawler"
    #TODO
    return vars(ap.parse_args())



def buildOutPath() -> str:
    cwd = getcwd()
    if (NAME not in cwd):
        perror(f"Not working from a standard directory ('{NAME}' expected), aborting")
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

    #TODO
    
    return









# ----------------------------------------------------------

if (__name__ == "__main__"):
    main()