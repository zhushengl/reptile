# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HungryspiderItem(scrapy.Item):
    shopName = scrapy.Field()
    address = scrapy.Field()
    rating = scrapy.Field()
    id = scrapy.Field()
    classification = scrapy.Field()
    foodInformation = scrapy.Field()
    pass
