import os
import re
import json
import scrapy
from utils import common
from urllib.parse import urlencode
from nested_lookup import nested_lookup
from inline_requests import inline_requests

from crawlers.items import EntityItem
from crawlers.items import ReviewItem

class BookingHotelService:
    def __init__(self):
        pass

    def getBaseReviewsUrl(self, hotel_url):
        cc1 = hotel_url.split("/")[-2]
        pagename = hotel_url.split("/")[-1].split(".")[0]
        params = {"cc1": cc1, "pagename": pagename, "rows": 10, "offset": 0}
        base_reviews_url = "https://www.booking.com/reviewlist.en-gb.html?" + urlencode(params)
        return base_reviews_url

    def getReviewItem(self, selector, url):
        item = ReviewItem()

        item["name"] = selector.xpath('//h3[@class="c-review-block__title"]/text()').get()
        item["description"] = " ".join(selector.xpath('//span[@class="c-review__body"]//text()').extract())
        item["rating"] = selector.xpath('//div[@class="bui-review-score__badge"]/text()').get()
        item["url"] = url

        return item

    def getHotelItem(self, response):
        item = EntityItem()

        data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())
        item["name"] = data["name"]
        item["address"] = data["address"]["streetAddress"]
        item["rating"] = data["aggregateRating"]["ratingValue"]/2

        data = eval(re.search(r'(?<=defaultCoordinates: )(\[.*\])(?=,)', response.text).group())
        item["latitude"] = data[0]
        item["longitude"] = data[1]

        item["properties"] = response.xpath('//div[contains(@class, "important_facility")]/text()').extract()
        item["description"] = " ".join(response.xpath('//div[@id="property_description_content"]//p//text()').extract())

        item["url"] = response.url

        return item

class BookingHotelsSpider(scrapy.Spider):
    name = "BookingHotels"
    start_urls = common.getStartUrls(name)

    def __init__(self):
        self.service = BookingHotelService()

    def parse(self, response):
        hotel_hrefs = list(map(lambda x: x.strip(), response.xpath('//a[@class="hotel_name_link url"]/@href').extract()))
        for href in hotel_hrefs[:2]:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parseHotel)

        # next_page_href = response.xpath('//li[@class="bui-pagination__item bui-pagination__next-arrow"]/a/@href').get()
        # if(next_page_href):
        #     url = response.urljoin(next_page_href)
        #     yield scrapy.Request(url, self.parse)

    @inline_requests
    def parseHotel(self, response):
        item = self.service.getHotelItem(response)

        base_reviews_url = self.service.getBaseReviewsUrl(response.url)
        response = yield scrapy.Request(base_reviews_url, headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"})

        reviews = []
        while(1):
            for review in self.parseReviews(response):
                reviews.append(review)

            break

            # next_page_href = response.xpath('//a[@class="pagenext"]/@href').get()
            # if(not next_page_href):
            #     break
            #
            # url = response.urljoin(next_page_href)
            # response = yield scrapy.Request(url)

        item["reviews"] = reviews
        yield item

    def parseReviews(self, response):
        review_selectors = response.xpath('//ul[@class="review_list"]//li')
        for review_selector in review_selectors:
            yield self.service.getReviewItem(scrapy.Selector(text = review_selector.extract()), response.url)
