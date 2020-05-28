import os
import json
import scrapy
from utils import common
from nested_lookup import nested_lookup
from inline_requests import inline_requests

from crawlers.items import EntityItem
from crawlers.items import ReviewItem

class TripAdvisorRestaurantService:
    def __init__(self):
        pass

    def getReviewItem(self, data):
        item = ReviewItem()

        item["name"] = data["name"]
        item["description"] = data["reviewBody"]
        item["rating"] = data["reviewRating"]["ratingValue"]
        item["url"] = data["url"]

        return item

    def getRestaurantItem(self, response):
        item = EntityItem()

        data = json.loads(response.css('script::text').re_first(r'window.__WEB_CONTEXT__=\{pageManifest:\s*(\{.*?)\}\s*;\s*'))

        x = data["redux"]["api"]["responses"]["/data/1.0/location/" + data["redux"]["route"]["detail"]]["data"]
        item["name"] = x["name"]
        item["properties"] = list(map(lambda d: d["name"], x["cuisine"]))
        item["description"] = x["description"] if "description" in x else ""
        item["address"] = x["address"]
        item["latitude"] = x["latitude"]
        item["longitude"] = x["longitude"]
        item["rating"] = x["rating"]

        item["url"] = response.url

        return item

class TripAdvisorRestaurantsSpider(scrapy.Spider):
    name = "TripAdvisorRestaurants"
    start_urls = common.getStartUrls(name)

    def __init__(self):
        self.service = TripAdvisorRestaurantService()

    def parse(self, response):
        hrefs = nested_lookup("detailPageUrl", json.loads(response.css('script::text').re_first(r'window.__WEB_CONTEXT__=\{pageManifest:\s*(\{.*?)\}\s*;\s*')))
        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parseRestaurant)

        next_page_href = response.xpath('//div[contains(@class, "pagination")]//a[contains(@class, "next")]/@href').get()
        if(next_page_href):
            url = response.urljoin(next_page_href)
            yield scrapy.Request(url, self.parse)

    @inline_requests
    def parseRestaurant(self, response):
        item = self.service.getRestaurantItem(response)

        reviews = []
        while(True):
            hrefs = response.xpath('//div[@class = "quote"]//a//@href').extract()
            for href in hrefs:
                url = response.urljoin(href)
                resp = yield scrapy.Request(url)
                review = dict(self.parseReview(resp))
                reviews.append(review)

            next_page_href = response.xpath('//div[contains(@class, "ui_pagination")]/a[contains(@class, "next")]/@href').get()
            if(not next_page_href):
                break

            url = response.urljoin(next_page_href)
            response = yield scrapy.Request(url)

        item["reviews"] = reviews
        yield item

    def parseReview(self, response):
        data = json.loads(response.xpath('//script[@type = "application/ld+json"]/text()').extract()[0].strip())
        data["url"] = response.url
        item = self.service.getReviewItem(data)
        return item
