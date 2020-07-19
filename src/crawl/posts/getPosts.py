import re
import sys
import json
import time
import tqdm
import argparse
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict, Union

from utils import common

class PostsCrawler:
    def __init__(self) -> None:
        self.retries = 5

    def getPageFromURL(self, url: str) -> BeautifulSoup:
        for i in range(self.retries):
            time.sleep(0.05)
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

    def getTitleFromPage(self, page: BeautifulSoup) -> str:
        try:
            for element in page(["script", "style"]):
                element.decompose()
            title = page.find("span", class_ = "topTitleText").get_text()
            title = re.sub("\s+", " ", title).strip()
            return title
        except:
            raise Exception("Error parsing HTML page for post title")

    def getQuestionFromPage(self, page: BeautifulSoup) -> str:
        try:
            for element in page(["script", "style"]):
                element.decompose()
            paragraphs = page.find("div", class_ = "postBody").findAll("p")
            question = " ".join(filter(None, [paragraph.get_text() for paragraph in paragraphs]))
            question = re.sub("\s+", " ", question).strip()
            return question
        except:
            raise Exception("Error parsing HTML page for post question")

    def getDateFromPage(self, page: BeautifulSoup) -> str:
        try:
            for element in page(["script", "style"]):
                element.decompose()
            date = page.find("div", class_ = "postDate").get_text()
            date = re.sub("\s+", " ", date).strip()
            return date
        except:
            raise Exception("Error parsing HTML page for post date")

    def getAnswersFromPage(self, page: BeautifulSoup) -> List[str]:
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

    def getPostFromURL(self, url: str) -> Dict[str, Union[str, List]]:
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

    def __call__(self, input_file_path: Path, output_file_path: Path) -> None:
        input_data = json.load(open(input_file_path, encoding = "utf-8"))

        output_data = []
        bar = tqdm.tqdm(total = sum([len(item["post_urls"]) for item in input_data.values()]))
        for city, item in input_data.items():
            for url in item["post_urls"]:
                try:
                    post = self.getPostFromURL(url)
                    post["city"] = city
                    output_data.append(post)
                except Exception as e:
                    pass
                    # print("Exception: %s on url %s" % (str(e), url))

                bar.update()

        bar.close()
        common.dumpJSON(output_data, output_file_path)

if(__name__ == "__main__"):
	project_root_path = common.getProjectRootPath()

	defaults = {}

	defaults["input_file_path"] = project_root_path / "data" / "generated" / "city_post_urls.json"
	defaults["output_file_path"] = project_root_path / "data" / "posts" / "raw" / "posts.raw.json"

	parser = argparse.ArgumentParser(description = "Crawl Posts from Trip Advisor")

	parser.add_argument("--input_file_path", type = str, default = defaults["input_file_path"])
	parser.add_argument("--output_file_path", type = str, default = defaults["output_file_path"])

	options = parser.parse_args(sys.argv[1:])

	posts_crawler = PostsCrawler()
	posts_crawler(input_file_path = Path(options.input_file_path), output_file_path = Path(options.output_file_path))
