import sys
import json
import tqdm
import logging
import argparse
from pathlib import Path
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from typing import List, Dict, Tuple

from .crawlers import Restaurants, Attractions, Hotels
from utils import common

logging.getLogger("scrapy").propagate = False

class TourqueEntitiesCrawler:
    def __init__(self) -> None:
        self.process = CrawlerProcess(settings = {"FEEDS": {"items.json": {"format": "json"},},})

    def fetch(self, data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        results = []
        bar = tqdm.tqdm(total = len(data))

        def crawler_results(signal, sender, item, response, spider):
            results.append(item)
            bar.update()

        dispatcher.connect(crawler_results, signal = signals.item_passed)
        self.process.crawl(Restaurants.Crawler, items = [item for item in data if item["id"].split("_")[1] == "R"])
        self.process.crawl(Hotels.Crawler, items = [item for item in data if item["id"].split("_")[1] == "H"])
        self.process.crawl(Attractions.Crawler, items = [item for item in data if item["id"].split("_")[1] == "A"])
        self.process.start()

        bar.close()
        return results

    def __call__(self, input_file_path: Path, output_dir_path: Path) -> None:
        data = []
        for item in json.load(open(input_file_path)):
            city = item["id"].split("_")[0]
            if(not (output_dir_path / city / item["id"]).with_suffix(".json").exists()):
                data.append(item)

        results = self.fetch(data)
        for result in results:
            city = result["id"].split("_")[0]
            output_file_path = (output_dir_path / city / result["id"]).with_suffix(".json")
            common.dumpJSON(result, output_file_path)

if(__name__ == "__main__"):
	project_root_path = common.getProjectRootPath()

	defaults = {}

	defaults["input_file_path"] = project_root_path / "data" / "tourque" / "support"/ "entity_ids_to_entity_urls_map.json"
	defaults["output_dir_path"] = project_root_path / "data" / "tourque" / "crawled"/ "entities"

	parser = argparse.ArgumentParser(description = "Crawl Questions from Trip Advisor")

	parser.add_argument("--input_file_path", type = str, default = defaults["input_file_path"])
	parser.add_argument("--output_dir_path", type = str, default = defaults["output_dir_path"])

	options = parser.parse_args(sys.argv[1:])

	tourque_entities_crawler = TourqueEntitiesCrawler()
	tourque_entities_crawler(input_file_path = Path(options.input_file_path), output_dir_path = Path(options.output_dir_path))
