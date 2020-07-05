import re
import sys
import bs4
import json
import time
import tqdm
import argparse
import urllib.request
from pathlib import Path
from typing import List, Dict, Tuple

from utils import common

class TourqueQuestionsCrawler:
    def __init__(self) -> None:
        self.retries = 5

    def getPageFromURL(self, url: str) -> bytes:
        for i in range(self.retries):
            time.sleep(0.01)
            try:
                response = urllib.request.urlopen(url)
                return response.read()
            except:
                pass
        raise Exception("Max Retries Exhausted")

    def getQuestionFromPage(self, page: bytes) -> str:
        try:
            soup = bs4.BeautifulSoup(page, "html.parser")
            for element in soup(["script", "style"]):
                element.decompose()
            paragraphs = soup.find("div", class_ = "postBody").findAll("p")
            question = " ".join(filter(None, [paragraph.get_text() for paragraph in paragraphs]))
            question = re.sub("\s+", " ", question).strip()
            return question
        except:
            raise Exception("Error parsing HTML page")

    def getQuestionFromURL(self, url: str) -> str:
        page = self.getPageFromURL(url = url)
        question = self.getQuestionFromPage(page = page)
        return question

    def __call__(self, input_file_path: Path, output_file_path: Path, log_file_path: Path) -> None:
        input_data = json.load(open(input_file_path))[:25]

        log_data = []
        output_data = []

        bar = tqdm.tqdm(total = len(input_data))
        for input_item in input_data:
            try:
                question = self.getQuestionFromURL(input_item["url"])
                status = "OK"
            except Exception as e:
                question = ""
                status = str(e)

            output_item = {}
            output_item["question"] = question
            output_item["url"] = input_item["url"]
            output_item["answer_entity_ids"] = input_item["answer_entity_ids"]
            output_data.append(output_item)

            log_item = {}
            log_item["url"] = input_item["url"]
            log_item["status"] = status
            log_data.append(log_item)

            bar.update()

        bar.close()
        common.dumpJSON(output_data, output_file_path)
        common.dumpJSON(log_data, log_file_path)

if(__name__ == "__main__"):
	project_root_path = common.getProjectRootPath()

	defaults = {}

	defaults["input_file_path"] = project_root_path / "data" / "tourque" / "support"/ "test_question_urls_to_answer_entity_ids_map.json"
	defaults["output_file_path"] = project_root_path / "data" / "tourque" / "crawled"/ "questions" / "test_questions.json"
	defaults["log_file_path"] = project_root_path / "data" / "tourque" / "logs"/ "questions" / "test_questions.log.json"

	parser = argparse.ArgumentParser(description = "Crawl Questions from Trip Advisor")

	parser.add_argument("--input_file_path", type = str, default = defaults["input_file_path"])
	parser.add_argument("--output_file_path", type = str, default = defaults["output_file_path"])
	parser.add_argument("--log_file_path", type = str, default = defaults["log_file_path"])

	options = parser.parse_args(sys.argv[1:])

	tourque_questions_crawler = TourqueQuestionsCrawler()
	tourque_questions_crawler(input_file_path = Path(options.input_file_path), output_file_path = Path(options.output_file_path), log_file_path = Path(options.log_file_path))
