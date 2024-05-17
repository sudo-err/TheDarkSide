from Scraper import Scraper
from Crawler import Crawler
from utils import *

from typing import Any, Dict
from argparse import ArgumentParser
from os import getcwd, mkdir
from os.path import isfile, isdir, join
from datetime import datetime

NAME = "TheDarkSide"

# ----------------------------------------------------------


def parseArgs() -> Dict[str,Any]:
    ap = ArgumentParser()
    ap.description = f"{NAME} - Dark web scraper and crawler"
    
    #? Args declarations
    ap.add_argument(
        "--mode","-m",
        default=None,
        type=str,
        choices=("scrape","crawl"),
        required=True,
        help="The mode to use, one of [scrape,crawl]"
    )
    ap.add_argument(
        "--list","-l",
        default=None,
        type=str,
        required=True,
        help="The file containing the list of URLs to scrape/crawl"
    )
    ap.add_argument(
        "--parallel", "-p",
        action='store_true',
        required=False,
        help="In scraping mode, performs the scraping in a parallel fashion (faster, but less responsive output)"
    )
    ap.add_argument(
        "--depth","-d",
        default=3,
        type=int,
        required=False,
        help="In crawling mode, sets the maximum depth the crawler goes (default: 3, max: 10)"
    )
    ap.add_argument(
        "--search","-s",
        nargs='+',
        default=None,
        type=str,
        required=False,
        help="In scraping mode, the list of terms to search for (case insensitive)"
    )
    ap.add_argument(
        "--output","-o",
        default=None,
        type=str,
        required=False,
        help="The name of the output file (will be saved in /out)"
    )
    ap.add_argument(
        "--tor-ports",
        nargs='+',
        default=[9050],
        type=int,
        required=False,
        help="The list of TOR ports in use (default: [9050])"
    )
    ap.add_argument(
        "--tor-cport",
        default=9051,
        type=int,
        required=False,
        help="The TOR control port in use (default: 9051)"
    )
    ap.add_argument(
        "--tor-autochange-id",
        default=1,
        type=int,
        required=False,
        help="The number of requests after wich TOR will change nodes (default: 1)"
    )

    #? Args checks
    args = vars(ap.parse_args())
    if (not isfile(args['list'])):
        perror(f"Invalid file: {args['list']}")
        exit(1)
    if (args['depth'] < 1) or (args['depth'] > 10):
        perror(f"Invalid depth: {args['depth']}")
        exit(1)
    if (args['mode'] == "scrape") and (args['search'] is None):
        perror(f"--search argument required in scraping mode")
        exit(1)
    if (args['output'] is None):
        args['output'] = datetime.now().strftime("%y-%m-%d_%H:%M")+".txt"
    for port in args['tor_ports']:
        if (port < 1024) or (port > 65535):
            perror(f"Invalid TOR port number: {port}")
            exit(1)
    args['tor_ports'] = tuple(args['tor_ports'])
    if (args['tor_cport'] < 1024) or (args["tor_cport"] > 65535):
        perror(f"Invalid TOR cport number: {args['tor_cport']}")
        exit(1)
    if (args['tor_autochange_id'] < 1):
        perror(f"Invalid autochange-id number: {args['tor_autochange_id']}")
        exit(1)
    
    return args


def buildOutDir() -> str:
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
    if (not isdir(out_path)):
        mkdir(out_path)
    return out_path



def main() -> None:
    out_dir = buildOutDir()
    args = parseArgs()

    mode:str = args['mode']
    url_list:list = readUrlList(args['list'])
    parallel:bool = args['parallel']
    depth:int = args['depth']
    search:list = args['search']
    out_path:str = join(out_dir,args['output'])

    tor_ports:tuple = args['tor_ports']
    tor_cport:int = args['tor_cport']
    autochange_id:int = args['tor_autochange_id']

    if (mode == "scrape"):
        scraper = Scraper(
            url_list=url_list,
            parallel=parallel,
            search=search,
            out_path=out_path,
            tor_ports=tor_ports,
            tor_cport=tor_cport,
            autochange_id=autochange_id
        )
        scraper.run()

    elif (mode == "crawl"):
        crawler = Crawler(
            url_list=url_list,
            depth=depth,
            out_path=out_path,
            tor_ports=tor_ports,
            tor_cport=tor_cport,
            autochange_id=autochange_id
        )
        crawler.run()
    
    return









# ----------------------------------------------------------

if (__name__ == "__main__"):
    main()