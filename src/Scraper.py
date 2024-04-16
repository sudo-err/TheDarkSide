from requests_tor import RequestsTor
from utils import *

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
        succ_errs = [0,0]

        if self.parallel:
            r_list = self.tor.get_urls(self.url_list)
            for r in r_list:
                if (not r.ok):
                    succ_errs[1] += 1
                    pwarning(f"{r.url} - {r.status_code}")
                    #appendOutput(self.out_path,f"[WARN] {r.url} - {r.status_code}\n")
                else:
                    succ_errs[0] += 1
                    content = r.text.lower()
                    for word in self.search:
                        if word.lower() in content:
                            pinfo(f"'{word}' FOUND: {r.url}")
                            appendOutput(self.out_path,f"'{word}' FOUND: {r.url}\n")

        else:
            for url in self.url_list:
                r = self.tor.get(url)
                if (not r.ok):
                    succ_errs[1] += 1
                    pwarning(f"{r.url} - {r.status_code}")
                    #appendOutput(self.out_path,f"[WARN] {r.url} - {r.status_code}\n")
                else:
                    succ_errs[0] += 1
                    content = r.text.lower()
                    for word in self.search:
                        if word.lower() in content:
                            pinfo(f"'{word}' FOUND: {r.url}")
                            appendOutput(self.out_path,f"'{word}' FOUND: {r.url}\n")

        pinfo(f"DONE: scraped {succ_errs[0]} URLs successfully, {succ_errs[1]} errors")
        #appendOutput(self.out_path,f"[INFO] DONE: scraped {succ} URLs successfully, {errs} errors\n")
        pinfo(f"Output file can be found in {self.out_path}")
        return 
