# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapyGenericPage(scrapy.Item):
    '''
    Stores generic page data and url
    '''
    url = scrapy.Field()
    title = scrapy.Field()
    site_title = scrapy.Field()
    description = scrapy.Field()
    raw_content = scrapy.Field()
    links = scrapy.Field()

class ScrapyCourseItem(scrapy.Item):
    '''
    Stores data about a course and associated subject
    SubItems: ScrapySectionItem, ScrapySubjectItem
    '''
    subject = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()

class ScrapyRedditPost(scrapy.Item):
    '''
    Stores data about a reddit post and its comments
    section
    '''
    url = scrapy.Field()
    title = scrapy.Field()
    subreddit = scrapy.Field()
    post_content = scrapy.Field()
    comments = scrapy.Field()
    links = scrapy.Field()
    