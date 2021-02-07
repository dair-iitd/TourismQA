import os
import json
import scrapy
from nested_lookup import nested_lookup
from inline_requests import inline_requests

from . import Processor

class Parser:
    def __init__(self):
        pass

    def getReviewItem(self, response):
        data = json.loads(response.xpath('//script[@type = "application/ld+json"]/text()').extract()[0].strip())

        item = {}

        item["title"] = data["name"]
        item["description"] = data["reviewBody"]
        item["rating"] = data["reviewRating"]["ratingValue"]
        item["date"] = response.xpath('//span[starts-with(@class, "ratingDate")]/@title').extract()[0]
        item["url"] = response.url

        return item

    def getEntityItem(self, response):
        item = {}

        data = json.loads(response.css('script::text').re_first(r'window.__WEB_CONTEXT__=\{pageManifest:\s*(\{.*?)\}\s*;\s*'))
        print(json.dumps(data, indent = 4), file = open("sorry", "w"))
        subdata = data["redux"]["api"]["responses"]["/data/1.0/location/" + data["redux"]["route"]["detail"]]["data"]

        item["name"] = subdata["name"]
        item["properties"] = list(map(lambda d: d["name"], subdata["cuisine"]))
        item["description"] = subdata["description"] if "description" in subdata else ""
        item["address"] = subdata["address"]
        item["latitude"] = subdata["latitude"]
        item["longitude"] = subdata["longitude"]
        item["rating"] = subdata["rating"]

        item["url"] = response.url

        return item

class Crawler(scrapy.Spider):
    def __init__(self, items):
        self.items = items
        self.parser = Parser()
        self.processor = Processor.Processor()

    def start_requests(self):
        for item in self.items:
            yield scrapy.Request(item["url"], meta = {"id": item["id"]})

    @inline_requests
    def parse(self, response):
        item = self.parser.getEntityItem(response)
        item["id"] = response.meta["id"]

        reviews = []
        while(1):
            hrefs = response.xpath('//div[@class = "quote"]//a//@href').extract()
            for href in hrefs:
                url = response.urljoin(href)
                res = yield scrapy.Request(url)
                review = self.parser.getReviewItem(res)
                reviews.append(review)

            next_page_href = response.xpath('//div[contains(@class, "ui_pagination")]/a[contains(@class, "next")]/@href').get()
            if(not next_page_href):
                break

            url = response.urljoin(next_page_href)
            response = yield scrapy.Request(url)

        item["reviews"] = reviews
        yield self.processor.processEntityItem(item)
