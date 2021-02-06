import re
import sys
import bs4
import time
import tqdm
import argparse
import urllib.request
from pathlib import Path

from utils import common

class TourqueQuestionsCrawler:
    def __init__(self, city_entities_file_path) -> None:
        self.retries = 5
        self.city_entities = common.loadJSON(city_entities_file_path)

    def getPageFromURL(self, url):
        for i in range(self.retries):
            time.sleep(0.01)
            try:
                response = urllib.request.urlopen(url)
                return response.read()
            except:
                pass
        raise Exception("Max Retries Exhausted")

    def getQuestionFromPage(self, page):
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

    def getQuestionFromURL(self, url):
        page = self.getPageFromURL(url = url)
        question = self.getQuestionFromPage(page = page)
        return question

    def convert(self, item):
        outitems = []

        question = item["question"]
        url = item["url"]
        answer_entity_ids = item["answer_entity_ids"]

        for answer_entity_id in answer_entity_ids:
            outitem = {}
            outitem["question"] = question
            outitem["url"] = url
            outitem["answer_entity_id"] = answer_entity_id
            outitem["answer_lat_long"] = self.city_entities[answer_entity_id.split("_")[0]][answer_entity_id]["location"]
            outitem["answer_entity_ids"] = answer_entity_ids
            outitems.append(outitem)

        return outitems

    def __call__(self, input_file_path, output_file_path):
        input_data = common.loadJSON(input_file_path)[:5]

        output_data = []

        bar = tqdm.tqdm(total = len(input_data))
        for input_item in input_data:
            try:
                question = self.getQuestionFromURL(input_item["url"])

                output_item = {}
                output_item["question"] = question
                output_item["url"] = input_item["url"]
                output_item["answer_entity_ids"] = input_item["answer_entity_ids"]

                output_data += self.convert(output_item)

            except Exception as e:
                print("Exception: %s on url %s" % (str(e), input_item["url"]))

            bar.update()

        bar.close()
        common.dumpJSON(output_data, output_file_path)

if(__name__ == "__main__"):
    project_root_path = common.getProjectRootPath()

    defaults = {}

    defaults["input_file_path"] = project_root_path / "data" / "tourque" / "posts" / "help" / "train_question_urls_to_answer_entity_ids.json"
    defaults["output_file_path"] = project_root_path / "data" / "tourque" / "posts" / "data" / "train.data.json"
    defaults["city_entities_file_path"] = project_root_path / "data" / "generated" / "city_entities.json"

    parser = argparse.ArgumentParser(description = "Crawl Data from Trip Advisor")

    parser.add_argument("--input_file_path", type = str, default = defaults["input_file_path"])
    parser.add_argument("--output_file_path", type = str, default = defaults["output_file_path"])
    parser.add_argument("--city_entities_file_path", type = str, default = defaults["city_entities_file_path"])

    options = parser.parse_args(sys.argv[1:])

    tourque_questions_crawler = TourqueQuestionsCrawler(city_entities_file_path = Path(options.city_entities_file_path))
    tourque_questions_crawler(input_file_path = Path(options.input_file_path), output_file_path = Path(options.output_file_path))
