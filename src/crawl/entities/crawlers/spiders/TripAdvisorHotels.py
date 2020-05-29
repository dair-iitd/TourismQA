import os
import json
import scrapy
from utils import common
from nested_lookup import nested_lookup
from inline_requests import inline_requests

from crawlers.items import EntityItem
from crawlers.items import ReviewItem

class TripAdvisorHotelService:
    def __init__(self):
        pass

    def getReviewItem(self, data):
        item = ReviewItem()

        item["name"] = data["title"]
        item["description"] = data["text"]
        item["rating"] = data["rating"]
        item["url"] = "https://www.tripadvisor.in" + data["url"]

        return item

    def getHotelItem(self, response):
        item = EntityItem()

        data = json.loads(response.css('script::text').re_first(r'window.__WEB_CONTEXT__=\{pageManifest:\s*(\{.*?)\}\s*;\s*'))

        x = nested_lookup("currentLocation", data)[0][0]
        item["name"] = x["name"]
        item["address"] = x["streetAddress"]["fullAddress"]
        item["latitude"] = x["latitude"]
        item["longitude"] = x["longitude"]

        x = list(filter(lambda l: (isinstance(l, list)) and (l != []) and (isinstance(l[0], dict)) and ("locationDescription" in l[0]), nested_lookup("locations", data)))[0][0]
        item["description"] = x["locationDescription"]
        item["properties"] = nested_lookup("amenityNameLocalized", x)
        item["rating"] = x["reviewSummary"]["rating"]

        item["url"] = response.url

        return item

class TripAdvisorHotelsSpider(scrapy.Spider):
    name = "TripAdvisorHotels"
    start_urls = common.getStartUrls(name)

    def __init__(self):
        self.service = TripAdvisorHotelService()

    def parse(self, response):
        hrefs = response.xpath('//div[@class = "listing_title"]//a//@href').extract()
        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parseHotel)

        next_page_href = response.xpath('//div[contains(@class, "ui_pagination")]//a[contains(@class, "next")]/@href').get()
        if(next_page_href):
            url = response.urljoin(next_page_href)
            yield scrapy.Request(url, self.parse)

    @inline_requests
    def parseHotel(self, response):
        item = self.service.getHotelItem(response)

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
        reviews = nested_lookup("reviews", json.loads(response.css('script::text').re_first(r'window.__WEB_CONTEXT__=\{pageManifest:\s*(\{.*?)\}\s*;\s*')))[0]
        for review in reviews:
            yield self.service.getReviewItem(review)
