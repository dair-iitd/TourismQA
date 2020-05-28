# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelSentimentItem(scrapy.Item):
	title = scrapy.Field()
	name = scrapy.Field()
	address= scrapy.Field()
	content = scrapy.Field()
	stars = scrapy.Field()
	num_rooms=scrapy.Field()
	hotel_class=scrapy.Field()
	amenity=scrapy.Field()
	review_rating=scrapy.Field()
	review_date=scrapy.Field()

class TripAdvisorReviewItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    review_stars = scrapy.Field()

    reviewer_id = scrapy.Field()
    reviewer_name = scrapy.Field()
    reviewer_level = scrapy.Field()
    reviewer_location = scrapy.Field()

    city = scrapy.Field()

    hotel_name = scrapy.Field()
    hotel_url = scrapy.Field()
    hotel_class = scrapy.Field()
    hotel_address = scrapy.Field()
    hotel_locality = scrapy.Field()
    hotel_review_stars = scrapy.Field()
    hotel_review_qty = scrapy.Field()

class AttractionSentimentItem(scrapy.Item):
	title = scrapy.Field()
	json=scrapy.Field()
	name = scrapy.Field()
	address= scrapy.Field()
	content = scrapy.Field()
	review_rating=scrapy.Field()
	review_date=scrapy.Field()
	type=scrapy.Field()
	description=scrapy.Field()
	
class RestaurantSentimentItem(scrapy.Item):
	title = scrapy.Field()
	json=scrapy.Field()
	name = scrapy.Field()
	address= scrapy.Field()
	content = scrapy.Field()
	review_rating=scrapy.Field()
	review_date=scrapy.Field()
	type=scrapy.Field()
	description=scrapy.Field()

class AttractionItem(scrapy.Item):
	name = scrapy.Field()
	address= scrapy.Field()
	type=scrapy.Field()
	description=scrapy.Field()

class RestaurantItem(scrapy.Item):
	name = scrapy.Field()
	address= scrapy.Field()
	type=scrapy.Field()
	description=scrapy.Field()
	
	
class BookingReviewItem(scrapy.Item):
    title = scrapy.Field()
    score = scrapy.Field()
    positive_content = scrapy.Field()
    negative_content = scrapy.Field()
    tags = scrapy.Field()
    url=scrapy.Field()
    hotel_name=scrapy.Field()
    address=scrapy.Field()
    review_date=scrapy.Field()
    hotel_class=scrapy.Field()
	
class BookingHotelItem(scrapy.Item):
    hotel_name = scrapy.Field()
    hotel_description= scrapy.Field()
    hotel_description_1= scrapy.Field()
    hotel_facilities = scrapy.Field()
    hotel_address = scrapy.Field()
    hotel_address_1 = scrapy.Field()