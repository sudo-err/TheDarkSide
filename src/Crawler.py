from requests_tor import RequestsTor
from requests.exceptions import ConnectionError
from utils import *
import re

class Crawler:

    def __init__(self, 
        url_list:list,
        depth:int, 
        out_path:str,
        retrieve_titles:bool=False,
        tor_ports:tuple=(9050,),
        tor_cport:int=9051,
        autochange_id:int=1 
    ) -> None:
        self.url_list = url_list
        self.depth = depth
        self.out_path = out_path
        self.retrieve_titles = retrieve_titles
        self.tor = RequestsTor(tor_ports=tor_ports,tor_cport=tor_cport,autochange_id=autochange_id)
        self.onionv2_regex = re.compile(r"\b[a-z2-7]{16}\.onion\b")
        self.onionv3_regex = re.compile(r"\b[a-z2-7]{56}\.onion\b")
        return



    def crawl(self, url:str, level:int, succ_errs:list, visited:set, found:set) -> None:

        if (level > self.depth):
            return
        
        if (url in visited):
            return
        
        pinfo(f"CRAWLING: {url} (depth = {level})")
        visited.add(url)

        try:
            r = self.tor.get(url)
        except ConnectionError:
            pwarning(f"Connection error: {url}")
            succ_errs[1] += 1
            return
        
        if (not r.ok):
            succ_errs[1] += 1
            pwarning(f"Status code {r.status_code}: {r.url}")
            return
        
        succ_errs[0] += 1
        content = r.text

        onion_v2 = self.onionv2_regex.findall(content)
        onion_v3 = self.onionv3_regex.findall(content)

        for v2 in onion_v2:
            if (v2 in found):
                continue
            appendOutput(self.out_path, f"{v2}\n")
            found.add(v2)
            if (level < self.depth):
                self.crawl("http://"+v2, level+1, succ_errs, visited, found)

        for v3 in onion_v3:
            if (v3 in found):
                continue
            appendOutput(self.out_path, f"{v3}\n")
            found.add(v3)
            if (level < self.depth):
                self.crawl("http://"+v3, level+1, succ_errs, visited, found)


    
    def crawl_verbose(self, url:str, level:int, succ_errs:list, visited:set, found:set) -> None:
        
        if (level > self.depth+1):
            return
        
        if (url in visited):
            return
        
        pinfo(f"CRAWLING: {url} (depth = {level})")
        visited.add(url)

        try:
            r = self.tor.get(url)
        except ConnectionError:
            pwarning(f"Connection error: {url}")
            succ_errs[1] += 1
            return
        
        if (not r.ok):
            succ_errs[1] += 1
            pwarning(f"Status code {r.status_code}: {r.url}")
            return
        
        succ_errs[0] += 1
        content = r.text
        title = "TITLE_NOT_FOUND"
        if ("<title" in content):
            tmp = re.search("<\W*title\W*(.*)</title",content,re.IGNORECASE)
            if (tmp is not None): title = tmp.group(1)

        appendOutput(self.out_path, f"{url} ({title})\n")

        onion_v2 = self.onionv2_regex.findall(content)
        onion_v3 = self.onionv3_regex.findall(content)

        for v2 in onion_v2:
            if (v2 in found):
                continue
            found.add(v2)
            if (level <= self.depth):
                self.crawl_verbose("http://"+v2, level+1, succ_errs, visited, found)

        for v3 in onion_v3:
            if (v3 in found):
                continue
            found.add(v3)
            if (level <= self.depth):
                self.crawl_verbose("http://"+v3, level+1, succ_errs, visited, found)



    def run(self) -> None:
        pinfo(f"Crawling from {len(self.url_list)} URLs")
        succ_errs = [0,0]
        visited = set()
        found = set()
        
        if self.retrieve_titles:
            for url in self.url_list:
                self.crawl_verbose(url, 0, succ_errs, visited, found)
        else:
            for url in self.url_list:
                self.crawl(url, 0, succ_errs, visited, found)
        
        print(f"[DONE] Crawled {succ_errs[0]} URLs successfully, {succ_errs[1]} errors")
        pinfo(f"Output file can be found in {self.out_path}")
        return
