import re
import sys
import bs4
import json
import math
import time
import tqdm
import logging
import argparse
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import OrderedDict
from typing import List, Dict, Union
from utils import common

class PostURLsCrawler:
    def __init__(self, sleep, retries, num_posts) -> None:
        self.sleep = sleep
        self.retries = retries
        self.num_posts = num_posts
        self.count = 0

    def getPageFromURL(self, url: str) -> BeautifulSoup:
        for i in range(self.retries):
            time.sleep(self.sleep)
            try:
                response = urllib.request.urlopen(url)
                page = BeautifulSoup(response.read(), "html.parser")
                return page
            except:
                pass
        raise Exception("Max Retries Exhausted for %s" % url)

    def getNextPage(self, url: str, page: BeautifulSoup) -> BeautifulSoup:
        next_page_elements = page.select('a[class*="pageNext"]')
        if(next_page_elements == []):
            return None
        next_page_url = urljoin(url, next_page_elements[0].get("href"))
        next_page = self.getPageFromURL(next_page_url)
        return next_page

    def getPostURLsFromPage(self, url: str, page: BeautifulSoup) -> List[str]:
        post_urls = []
        posts = page.find("table", attrs = {"class": "topics"}).findAll("tr")[1:]
        for post in posts:
            try:
                x = post.find("td").find("img")
                if(x is not None and x.get("alt").lower() == "sticky"):
                    continue
                x = post.find("a")
                if(x is not None):
                    post_url = urljoin(url, x.get("href"))
                    post_urls.append(post_url)
                    self.count += 1
                    if(self.count == self.num_posts):
                        break
            except:
                pass
        return post_urls

    def getPostURLsFromCityURL(self, city_url: str) -> List[str]:
        post_urls = []
        try:
            page = self.getPageFromURL(url = city_url)

            while(page is not None):
                post_urls_ = self.getPostURLsFromPage(url = city_url, page = page)
                post_urls += post_urls_
                if(len(post_urls) == self.num_posts):
                    break
                page = self.getNextPage(url = url, page = page)
        except:
            pass
        return post_urls

    def __call__(self, city_urls_file_path: Path, city_post_urls_file_path: Path) -> None:
        city_post_urls = OrderedDict()
        city_urls = json.load(open(city_urls_file_path))

        bar = tqdm.tqdm(total = len(city_urls))
        for city, city_url in city_urls.items():
            self.count = 0
            post_urls = self.getPostURLsFromCityURL(city_url = city_url)

            city_post_urls[city] = {}
            city_post_urls[city]["city_url"] = city_url
            city_post_urls[city]["post_urls"] = post_urls

            bar.update()

        bar.close()
        common.dumpJSON(city_post_urls, city_post_urls_file_path)

if(__name__ == "__main__"):
    project_root_path = common.getProjectRootPath()

    defaults = {}

    defaults["city_urls_file_path"] = project_root_path / "data" / "common" / "city_urls.posts.json"
    defaults["city_post_urls_file_path"] = project_root_path / "data" / "generated" / "city_post_urls.json"
    defaults["sleep"] = 0.05
    defaults["retries"] = 5
    defaults["num_posts"] = 15

    parser = argparse.ArgumentParser(description = "Crawl city posts url from Trip Advisor")

    parser.add_argument("--city_urls_file_path", type = str, default = defaults["city_urls_file_path"])
    parser.add_argument("--city_post_urls_file_path", type = str, default = defaults["city_post_urls_file_path"])
    parser.add_argument("--sleep", type = float, default = defaults["sleep"])
    parser.add_argument("--retries", type = int, default = defaults["retries"])
    parser.add_argument("--num_posts", type = int, default = defaults["num_posts"])

    options = parser.parse_args(sys.argv[1:])

    post_urls_crawler = PostURLsCrawler(sleep = options.sleep, retries = options.retries, num_posts = options.num_posts)
    post_urls_crawler(city_urls_file_path = Path(options.city_urls_file_path), city_post_urls_file_path = Path(options.city_post_urls_file_path))
