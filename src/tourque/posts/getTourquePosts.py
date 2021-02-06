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

class TourquePostsCrawler:
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
            raise Exception("Error parsing HTML page for Title")

    def getQuestionFromPage(self, page):
        try:
            for element in page(["script", "style"]):
                element.decompose()
            paragraphs = page.find("div", class_ = "postBody").findAll("p")
            question = " ".join(filter(None, [paragraph.get_text() for paragraph in paragraphs]))
            question = re.sub("\s+", " ", question).strip()
            return question
        except:
            raise Exception("Error parsing HTML page for Question")

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

        while(page is not None):
            answers = self.getAnswersFromPage(page = page)
            post["answers"] += answers
            page = self.getNextPage(url = url, page = page)

        return post

    def __call__(self, input_file_path, output_file_path, cities_file_path):
        cities = common.loadJSON(cities_file_path)
        input_data = common.loadJSON(input_file_path)[:5]

        output_data = []
        bar = tqdm.tqdm(total = len(input_data))
        for input_item in input_data:
            try:
                post = self.getPostFromURL(input_item["url"])
                post["city"] = cities[int(input_item["answer_entity_ids"][0].split("_")[0])]
                output_data.append(post)
            except Exception as e:
                print("Exception: %s on url %s" % (str(e), input_item["url"]))

            bar.update()

        bar.close()
        common.dumpJSON(output_data, output_file_path)

if(__name__ == "__main__"):
    project_root_path = common.getProjectRootPath()

    defaults = {}

    defaults["input_file_path"] = project_root_path / "data" / "tourque" / "posts" / "help"/ "train_question_urls_to_answer_entity_ids.json"
    defaults["output_file_path"] = project_root_path / "data" / "tourque" / "posts" / "data" / "train.posts.json"
    defaults["cities_file_path"] = project_root_path / "data" / "common" / "cities.json"

    parser = argparse.ArgumentParser(description = "Crawl Posts from Trip Advisor")

    parser.add_argument("-i", "--input_file_path", type = str, default = defaults["input_file_path"])
    parser.add_argument("-o", "--output_file_path", type = str, default = defaults["output_file_path"])
    parser.add_argument("-c", "--cities_file_path", type = str, default = defaults["cities_file_path"])

    options = parser.parse_args(sys.argv[1:])

    tourque_posts_crawler = TourquePostsCrawler()
    tourque_posts_crawler(input_file_path = Path(options.input_file_path), output_file_path = Path(options.output_file_path), cities_file_path = Path(options.cities_file_path))
