# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapyGenericPage(scrapy.Item):
    """
    Stores generic page data and url
    """
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    raw_content = scrapy.Field()

class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
