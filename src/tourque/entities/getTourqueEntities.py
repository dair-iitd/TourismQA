import sys
import json
import tqdm
import logging
import argparse
from pathlib import Path
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

from utils import common
from utils.crawlers import Restaurants, Attractions, Hotels

logging.getLogger("scrapy").propagate = False

class TourqueEntitiesCrawler:
    def __init__(self) -> None:
        self.process = CrawlerProcess(settings = {"FEEDS": {"items.json": {"format": "json"},},})

    def fetch(self, data):
        results = []
        bar = tqdm.tqdm(total = len(data))

        def fetcher(signal, sender, item, response, spider):
            results.append(item)
            bar.update()

        dispatcher.connect(fetcher, signal = signals.item_passed)

        self.process.crawl(Restaurants.Crawler, items = list(filter(lambda item: item["id"].split("_")[1] == "R", data)))
        self.process.crawl(Hotels.Crawler, items = list(filter(lambda item: item["id"].split("_")[1] == "H", data)))
        self.process.crawl(Attractions.Crawler, items = list(filter(lambda item: item["id"].split("_")[1] == "A", data)))

        self.process.start()

        bar.close()
        return results

    def __call__(self, input_file_path, output_dir_path):
        data = []

        for item in common.loadJSON(input_file_path):
            if(not (output_dir_path / item["id"].split("_")[0] / item["id"]).with_suffix(".json").exists()):
                data.append(item)

        for item in self.fetch(data):
            common.dumpJSON(item, (output_dir_path / item["id"].split("_")[0] / item["id"]).with_suffix(".json"))

if(__name__ == "__main__"):
    project_root_path = common.getProjectRootPath()

    defaults = {}

    defaults["input_file_path"] = project_root_path / "data" / "tourque" / "entities" / "help"/ "entity_ids_to_entity_urls.json"
    defaults["output_dir_path"] = project_root_path / "data" / "tourque" / "entities" / "data"

    parser = argparse.ArgumentParser(description = "Crawl Questions from Trip Advisor")

    parser.add_argument("-i", "--input_file_path", type = str, default = defaults["input_file_path"])
    parser.add_argument("-o", "--output_dir_path", type = str, default = defaults["output_dir_path"])

    options = parser.parse_args(sys.argv[1:])

    tourque_entities_crawler = TourqueEntitiesCrawler()
    tourque_entities_crawler(input_file_path = Path(options.input_file_path), output_dir_path = Path(options.output_dir_path))
