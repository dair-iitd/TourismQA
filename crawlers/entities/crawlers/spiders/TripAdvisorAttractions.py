import os
import json
import scrapy
from utils import common
from nested_lookup import nested_lookup
from inline_requests import inline_requests

from crawlers.items import EntityItem
from crawlers.items import ReviewItem

class TripAdvisorAttractionService:
    def __init__(self):
        pass

    def getReviewItem(self, data):
        item = ReviewItem()

        item["name"] = data["title"]
        item["description"] = data["text"]
        item["rating"] = data["rating"]
        item["url"] = "https://www.tripadvisor.in" + data["url"]

        return item

    def getAttractionItem(self, response):
        item = EntityItem()

        data = json.loads(response.css('script::text').re_first(r'window.__WEB_CONTEXT__=\{pageManifest:\s*(\{.*?)\}\s*;\s*'))

        id = data["redux"]["route"]["detail"]

        x = data["redux"]["api"]["responses"]["/data/1.0/location/" + id]["data"]
        item["name"] = x["name"]
        item["address"] = x["address"]
        item["latitude"] = x["latitude"]
        item["longitude"] = x["longitude"]
        item["rating"] = x["rating"]

        x = data["redux"]["api"]["responses"]["/data/1.0/attraction/about/" + id]["data"]
        item["properties"] = list(map(lambda d: d["name"], x["taxonomyInfos"]))
        item["description"] = x["description"]["text"] if "description" in x else ""

        item["url"] = response.url

        return item

class TripAdvisorAttractionsSpider(scrapy.Spider):
    name = "TripAdvisorAttractions"
    start_urls = common.getStartUrls(name)

    def __init__(self):
        self.service = TripAdvisorAttractionService()

    def parse(self, response):
        hrefs = response.xpath('//div[starts-with(@class, "tracking_attraction_title")]/a/@href').extract()
        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parseAttraction)

        next_page_href = response.xpath('//div[@class = "pagination"]//a[contains(@class, "next")]/@href').get()
        if(next_page_href):
            url = response.urljoin(next_page_href)
            yield scrapy.Request(url, self.parse)

    @inline_requests
    def parseAttraction(self, response):
        item = self.service.getAttractionItem(response)

        reviews = []
        while(1):
            for review in self.parseReviews(response):
                reviews.append(dict(review))

            next_page_href = response.xpath('//div[contains(@class, "ui_pagination")]/a[contains(@class, "next")]/@href').get()
            if(not next_page_href):
                break

            url = response.urljoin(next_page_href)
            response = yield scrapy.Request(url)

        item["reviews"] = reviews
        yield item

    def parseReviews(self, response):
        reviews = nested_lookup("reviewListPage", json.loads(response.css('script::text').re_first(r'window.__WEB_CONTEXT__=\{pageManifest:\s*(\{.*?)\}\s*;\s*')))[0]["reviews"]
        for review in reviews:
            yield self.service.getReviewItem(review)
