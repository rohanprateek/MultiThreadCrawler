# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 13:36:38 2021

@author: Rohan Prateek
"""

print('Importing Libraries..')
import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import os
from pathlib import Path

class MultiThreadScraper:
    def __init__(self, base_url, no_pages=250):
        
        self.base_url = base_url
        self.root_url = '{}://{}'.format(urlparse(self.base_url).scheme, urlparse(self.base_url).netloc)
        self.pool = ThreadPoolExecutor(max_workers=20)
        self.scraped_pages = set([])
        self.to_crawl = Queue()
        self.to_crawl.put(self.base_url)
        self.create_dir()
        self.page_count = no_pages

    def parse_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            url = link['href']
            if url.startswith('/') or url.startswith(self.root_url):
                url = urljoin(self.root_url, url)
                if url not in self.scraped_pages:
                    self.to_crawl.put(url)
                

    def scrape_info(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        data = ''.join(soup.strings)
        file_name = Path(url).parts[-1]
        path = self.data_path + "\\" + file_name + ".txt"
        file = open(path, 'w', encoding='utf8')
        file.write(data)
        file.close()
        return 
    
    def create_dir(self):
        try:
            parent = os.getcwd()
            folder = 'scrapedata'
            self.data_path = os.path.join(parent, folder)
            os.mkdir(self.data_path)
        except:
            pass    
        return 
    
    def post_scrape_callback(self, res):
        result = res.result()
        if result and result.status_code == 200:
            self.parse_links(result.text)
            self.scrape_info(result.text, result.url)
        
    def scrape_page(self, url):
        try:
            res = requests.get(url, timeout=(3, 30))
            return res
        except requests.RequestException:
            return 
            
    def run_scraper(self):
        i = self.page_count
        while i:
            i -= 1
            try:
                target_url = self.to_crawl.get(timeout=60)
                if target_url not in self.scraped_pages:
                    print("Scraping URL: {}".format(target_url))
                    self.scraped_pages.add(target_url)
                    job = self.pool.submit(self.scrape_page, target_url)
                    job.add_done_callback(self.post_scrape_callback)
                    
            except Empty:
                return 
        
            except Exception as e:
                print(e)
                continue
        
if __name__ == '__main__':
    url = input("Enter the URL of the starting page: ")
    n = int(input("Enter the number of pages to be scraped(default = 250): "))
    s = MultiThreadScraper(url, n)
    s.run_scraper() 