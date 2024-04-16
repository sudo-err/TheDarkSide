from requests_tor import RequestsTor
from utils import *
import re

class Crawler:

    def __init__(self, 
        url_list:list,
        depth:int, 
        out_path:str,
        tor_ports:tuple=(9050,),
        tor_cport:int=9051,
        autochange_id:int=1 
    ) -> None:
        self.url_list = url_list
        self.depth = depth
        self.out_path = out_path
        self.tor = RequestsTor(tor_ports=tor_ports,tor_cport=tor_cport,autochange_id=autochange_id)
        self.onionv2_regex = re.compile(r"\b[a-z2-7]{16}\.onion\b")
        self.onionv3_regex = re.compile(r"\b[a-z2-7]{56}\.onion\b")
        return

    def crawl(self, url:str, level:int, succ_errs:list) -> None:
        if (level > self.depth):
            pinfo("Maximum depth reached, crawler stopping")
            #appendOutput(self.out_path,f"[INFO] Maximum depth reached, crawler stopping")
            return
        pinfo(f"CRAWLING: {url}")
        #appendOutput(self.out_path,f"[INFO] Crawling: {url}")
        r = self.tor.get(url)
        if (not r.ok):
            succ_errs[1] += 1
            pwarning(f"{r.url} - {r.status_code}")
            #appendOutput(self.out_path,f"[WARN] {r.url} - {r.status_code}\n")
            return
        else:
            succ_errs[0] += 1
            content = r.text
            onion_v2 = self.onionv2_regex.findall(content)
            onion_v3 = self.onionv3_regex.findall(content)
            for v2 in onion_v2:
                appendOutput(self.out_path,f"{v2}\n")
                self.crawl(v2,level+1,succ_errs)
            for v3 in onion_v3:
                appendOutput(self.out_path,f"{v3}\n")
                self.crawl(v3,level+1,succ_errs)

    def run(self) -> None:
        pinfo(f"Crawling {len(self.url_list)} URLs")
        succ_errs = [0,0]
        for url in self.url_list:
            self.crawl(url, 0, succ_errs)
        pinfo(f"DONE: crawled {succ_errs[0]} URLs successfully, {succ_errs[1]} errors")
        #appendOutput(self.out_path,f"[INFO] DONE: crawled {succ_errs[0]} URLs successfully, {succ_errs[1]} errors")
        pinfo(f"Output file can be found in {self.out_path}")
        return
