import re
import sys
import time
import tqdm
import argparse
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from utils import common

class PostsCrawler:
    def __init__(self):
        self.retries = 5

    def getPageFromURL(self, url):
        for i in range(self.retries):
            time.sleep(0.05)
            try:
                response = urllib.request.urlopen(url)
                page = BeautifulSoup(response.read(), "html.parser")
                return page
            except:
                pass
        raise Exception("Max Retries Exhausted for %s" % url)

    def getNextPage(self, url, page):
        next_page_elements = page.select('a[class*="pageNext"]')
        if(next_page_elements == []):
            return None
        next_page_url = urljoin(url, next_page_elements[0].get("href"))
        next_page = self.getPageFromURL(next_page_url)
        return next_page

    def getTitleFromPage(self, page):
        try:
            for element in page(["script", "style"]):
                element.decompose()
            title = page.find("span", class_ = "topTitleText").get_text()
            title = re.sub("\s+", " ", title).strip()
            return title
        except:
            raise Exception("Error parsing HTML page for post title")

    def getQuestionFromPage(self, page):
        try:
            for element in page(["script", "style"]):
                element.decompose()
            paragraphs = page.find("div", class_ = "postBody").findAll("p")
            question = " ".join(filter(None, [paragraph.get_text() for paragraph in paragraphs]))
            question = re.sub("\s+", " ", question).strip()
            return question
        except:
            raise Exception("Error parsing HTML page for post question")

    def getDateFromPage(self, page):
        try:
            for element in page(["script", "style"]):
                element.decompose()
            date = page.find("div", class_ = "postDate").get_text()
            date = re.sub("\s+", " ", date).strip()
            return date
        except:
            raise Exception("Error parsing HTML page for post date")

    def getAnswersFromPage(self, page):
        try:
            answers = []

            for element in page(["script", "style"]):
                element.decompose()

            elements = page.findAll("div", class_ = "postcontent")[1:]
            for element in elements:
                date = element.find("div", class_ = "postDate").get_text()
                date = re.sub("\s+", " ", date).strip()

                paragraphs = element.find("div", class_ = "postBody").findAll("p")
                body = " ".join(filter(None, [paragraph.get_text() for paragraph in paragraphs]))
                body = re.sub("\s+", " ", body).strip()

                if("Message from Tripadvisor staff" not in body):
                    answers.append({"date": date, "body": body})

            return answers
        except:
            raise Exception("Error parsing HTML page for Answers")

    def getPostFromURL(self, url):
        post = {"url": url, "title": "", "question": "", "answers" : []}

        page = self.getPageFromURL(url = url)

        post["title"] = self.getTitleFromPage(page = page)
        post["question"] = self.getQuestionFromPage(page = page)
        post["date"] = self.getDateFromPage(page = page)

        if(all((" %s " % indicator) not in post["question"].lower() for indicator in ["recommend", "suggest", "place to", "where", "option", "best"])):
            raise Exception("Irrelevant post")

        while(page is not None):
            answers = self.getAnswersFromPage(page = page)
            post["answers"] += answers
            page = self.getNextPage(url = url, page = page)

        return post

    def __call__(self, posts_urls_file_path, posts_file_path):
        posts_urls = common.loadJSON(posts_urls_file_path)

        posts = []
        bar = tqdm.tqdm(total = sum([len(item["post_urls"]) for item in posts_urls.values()]))
        for city, item in posts_urls.items():
            for url in item["post_urls"]:
                try:
                    post = self.getPostFromURL(url)
                    post["city"] = city
                    posts.append(post)
                except Exception as e:
                    pass

                bar.update()

        bar.close()
        common.dumpJSON(posts, posts_file_path)

if(__name__ == "__main__"):
	project_root_path = common.getProjectRootPath()

	defaults = {}

	defaults["posts_urls_file_path"] = project_root_path / "data" / "custom" / "posts" / "urls" / "posts.urls.json"
	defaults["posts_file_path"] = project_root_path / "data" / "custom" / "posts" / "fetched" / "posts.fetched.json"

	parser = argparse.ArgumentParser(description = "Crawl Posts from Trip Advisor")

	parser.add_argument("--posts_urls_file_path", type = str, default = defaults["posts_urls_file_path"])
	parser.add_argument("--posts_file_path", type = str, default = defaults["posts_file_path"])

	options = parser.parse_args(sys.argv[1:])

	posts_crawler = PostsCrawler()
	posts_crawler(posts_urls_file_path = Path(options.posts_urls_file_path), posts_file_path = Path(options.posts_file_path))
