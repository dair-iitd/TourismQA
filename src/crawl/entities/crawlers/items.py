# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class EntityItem(scrapy.Item):
	name = scrapy.Field()
	properties = scrapy.Field()
	description = scrapy.Field()
	address = scrapy.Field()
	latitude = scrapy.Field()
	longitude = scrapy.Field()
	rating = scrapy.Field()
	url = scrapy.Field()
	reviews = scrapy.Field()

class ReviewItem(scrapy.Item):
	name = scrapy.Field()
	description = scrapy.Field()
	rating = scrapy.Field()
	url = scrapy.Field()
