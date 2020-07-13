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

class TourquePostsCrawler:
    def __init__(self) -> None:
        self.retries = 5

    def getPageFromURL(self, url: str) -> bytes:
        for i in range(self.retries):
            time.sleep(0.01)
            try:
                response = urllib.request.urlopen(url)
                page = BeautifulSoup(response.read(), "html.parser")
                return page
            except:
                pass
        raise Exception("Max Retries Exhausted")

    def getNextPage(self, url: str, page: BeautifulSoup) -> BeautifulSoup:
        next_page_elements = page.select('a[class*="pageNext"]')
        if(next_page_elements == []):
            return None
        next_page_url = urljoin(url, next_page_elements[0].get("href"))
        next_page = self.getPageFromURL(next_page_url)
        return next_page

    def getQuestionFromPage(self, page: BeautifulSoup) -> str:
        try:
            for element in page(["script", "style"]):
                element.decompose()
            paragraphs = page.find("div", class_ = "postBody").findAll("p")
            question = " ".join(filter(None, [paragraph.get_text() for paragraph in paragraphs]))
            question = re.sub("\s+", " ", question).strip()
            return question
        except:
            raise Exception("Error parsing HTML page for Question")

    def getAnswersFromPage(self, page: BeautifulSoup) -> List[str]:
        try:
            for element in page(["script", "style"]):
                element.decompose()
            elements = page.findAll("div", class_ = "postBody")[1:]
            answers = []
            for element in elements:
                paragraphs = element.findAll("p")
                answer = " ".join(filter(None, [paragraph.get_text() for paragraph in paragraphs]))
                answer = re.sub("\s+", " ", answer).strip()
                if("Message from Tripadvisor staff" not in answer):
                    answers.append(answer)
            return answers
        except:
            raise Exception("Error parsing HTML page for Answers")

    def getPostFromURL(self, url: str) -> Dict[str, Union[str, List]]:
        post = {"question": "", "answers" : []}

        page = self.getPageFromURL(url = url)
        post["question"] = self.getQuestionFromPage(page = page)

        while(page is not None):
            answers = self.getAnswersFromPage(page = page)
            post["answers"] += answers
            page = self.getNextPage(url = url, page = page)

        return post

    def __call__(self, input_file_path: Path, output_file_path: Path) -> None:
        input_data = json.load(open(input_file_path))[:10]

        output_data = []

        bar = tqdm.tqdm(total = len(input_data))
        for input_item in input_data:
            try:
                post = self.getPostFromURL(input_item["url"])

                output_item = {}
                output_item["question"] = post["question"]
                output_item["answers"] = post["answers"]
                output_item["url"] = input_item["url"]
                output_data.append(output_item)
            except Exception as e:
                print("Exception: %s on url %s" % (str(e), input_item["url"]))

            bar.update()

        bar.close()
        common.dumpJSON(output_data, output_file_path)

if(__name__ == "__main__"):
	project_root_path = common.getProjectRootPath()

	defaults = {}

	defaults["input_file_path"] = project_root_path / "data" / "tourque" / "support"/ "test_question_urls_to_answer_entity_ids_map.json"
	defaults["output_file_path"] = project_root_path / "data" / "tourque" / "crawled"/ "posts" / "test_posts.json"

	parser = argparse.ArgumentParser(description = "Crawl Posts from Trip Advisor")

	parser.add_argument("--input_file_path", type = str, default = defaults["input_file_path"])
	parser.add_argument("--output_file_path", type = str, default = defaults["output_file_path"])

	options = parser.parse_args(sys.argv[1:])

	tourque_posts_crawler = TourquePostsCrawler()
	tourque_posts_crawler(input_file_path = Path(options.input_file_path), output_file_path = Path(options.output_file_path))
