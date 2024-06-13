from requests_tor import RequestsTor
from requests.exceptions import ConnectionError
from utils import *
import re

class Scraper:

    def __init__(self, 
        url_list:list,
        parallel:bool,
        search:list, 
        out_path:str,
        tor_ports:tuple=(9050,),
        tor_cport:int=9051,
        autochange_id:int=1
    ) -> None:
        self.url_list = url_list
        self.parallel = parallel
        self.search = search
        self.out_path = out_path
        self.tor = RequestsTor(tor_ports=tor_ports,tor_cport=tor_cport,autochange_id=autochange_id)
        return



    def run(self) -> None:

        pinfo(f"Scraping {len(self.url_list)} URLs")
        succ_errs = [0,0]

        if self.parallel:
            r_list = self.tor.get_urls(self.url_list)
            for r in r_list:

                if (not r.ok):
                    succ_errs[1] += 1
                    pwarning(f"Status code {r.status_code}: {r.url}")
                    continue

                succ_errs[0] += 1
                content = r.text
                title = "NAME_NOT_FOUND"
                if ("<title" in content):
                    tmp = re.search("<\W*title\W*(.*)</title",content,re.IGNORECASE)
                    if (tmp is not None): title = tmp.group(1)
                pinfo(f"SCRAPING: {url} ({title})")

                for word in self.search:
                    if word.lower() in content.lower():
                        print(f"[FOUND] '{word}': {r.url} ({title})")
                        appendOutput(self.out_path,f"[FOUND] '{word}': {r.url} ({title})\n")

        else:
            for url in self.url_list:

                try:
                    r = self.tor.get(url)
                except ConnectionError:
                    pwarning(f"Connection error: {url}")
                    succ_errs[1] += 1
                    continue

                if (not r.ok):
                    succ_errs[1] += 1
                    pwarning(f"Status code {r.status_code}: {r.url}")
                    continue

                succ_errs[0] += 1
                content = r.text
                title = "TITLE_NOT_FOUND"
                if ("<title" in content):
                    tmp = re.search("<\W*title\W*(.*)</title",content,re.IGNORECASE)
                    if (tmp is not None): title = tmp.group(1)
                pinfo(f"SCRAPING: {url} ({title})")

                for word in self.search:
                    if word.lower() in content.lower():
                        print(f"[FOUND] '{word}': {r.url} ({title})")
                        appendOutput(self.out_path,f"[FOUND] '{word}': {r.url} ({title})\n")

        print(f"[DONE] Scraped {succ_errs[0]} URLs successfully, {succ_errs[1]} errors")
        pinfo(f"Output file can be found in {self.out_path}")
        return 
