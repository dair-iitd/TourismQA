import os
import json
import scrapy
from utils import common
from nested_lookup import nested_lookup
from inline_requests import inline_requests

from . import Processor

class Service:
    def __init__(self):
        pass

    def getReviewItem(self, data):
        item = {}

        item["title"] = data["title"]
        item["description"] = data["text"]
        item["rating"] = data["rating"]
        item["date"] = data["publishedDate"]
        item["url"] = "https://www.tripadvisor.in" + data["url"]

        return item

    def getEntityItem(self, response):
        item = {}

        data = json.loads(response.css('script::text').re_first(r'window.__WEB_CONTEXT__=\{pageManifest:\s*(\{.*?)\}\s*;\s*'))
        id = data["redux"]["route"]["detail"]

        subdata = data["redux"]["api"]["responses"]["/data/1.0/location/" + id]["data"]
        item["name"] = subdata["name"]
        item["address"] = subdata["address"]
        item["latitude"] = subdata["latitude"]
        item["longitude"] = subdata["longitude"]
        item["rating"] = subdata["rating"]

        subdata = data["redux"]["api"]["responses"]["/data/1.0/attraction/about/" + id]["data"]
        item["properties"] = list(map(lambda d: d["name"], subdata["taxonomyInfos"]))
        item["description"] = subdata["description"]["text"] if "description" in subdata else ""
        item["url"] = response.url

        return item

class Crawler(scrapy.Spider):
    def __init__(self, items):
        self.items = items
        self.service = Service()
        self.processor = Processor.Processor()

    def start_requests(self):
        for item in self.items:
            yield scrapy.Request(item["url"], meta = {"id": item["id"]})

    def getReviewItems(self, response):
        reviews = nested_lookup("reviewListPage", json.loads(response.css('script::text').re_first(r'window.__WEB_CONTEXT__=\{pageManifest:\s*(\{.*?)\}\s*;\s*')))[0]["reviews"]
        for review in reviews:
            yield self.service.getReviewItem(review)

    @inline_requests
    def parse(self, response):
        item = self.service.getEntityItem(response)
        item["id"] = response.meta["id"]

        reviews = []
        while(1):
            for review in self.getReviewItems(response):
                reviews.append(review)

            next_page_href = response.xpath('//div[contains(@class, "ui_pagination")]/a[contains(@class, "next")]/@href').get()
            if(not next_page_href):
                break

            url = response.urljoin(next_page_href)
            response = yield scrapy.Request(url)

        item["reviews"] = reviews
        yield self.processor.processEntityItem(item)
