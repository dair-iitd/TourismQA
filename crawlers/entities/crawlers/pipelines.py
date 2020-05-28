# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
from utils import processing

class CrawlersPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        crawled_dir_path = "data"
        if(not os.path.exists(crawled_dir_path)):
            os.makedirs(crawled_dir_path)

        self.crawled_file_path = os.path.join(crawled_dir_path, spider.name + ".txt")
        self.json_file_path =  os.path.join(crawled_dir_path, spider.name + ".json")

        self.crawled_file = open(self.crawled_file_path, "a")

    def close_spider(self, spider):
        self.crawled_file.close()
        data = [json.loads(line) for line in open(self.crawled_file_path, "r").readlines()]
        json.dump(data, open(self.json_file_path, "w"), indent = 4, ensure_ascii = False)

    def process_item(self, item, spider):
        processed_item = processing.processEntityItem(dict(item))
        self.crawled_file.write(json.dumps(processed_item))
        self.crawled_file.write("\n")
        return processed_item
