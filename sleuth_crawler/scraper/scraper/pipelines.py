# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, time, datetime
from sleuth_backend.views.views import SOLR
from sleuth_backend.solr.models import *
from sleuth_crawler.scraper.scraper.items import *

class SolrPipeline(object):
    """
    Process item and store in Solr
    """
    def __init__(self, solr_connection=SOLR):
        self.solr_connection = solr_connection

    def close_spider(self, spider=None):
        '''
        Defragment Solr database after spider completes task
        '''
        print("Closing scraper: Emptying all queued documents")
        self.solr_connection.insert_queued()
        print("Closing scraper: Optimizing all cores")
        self.solr_connection.optimize()

    def process_item(self, item, spider=None):
        '''
        Match item type to predefined Schemas
        https://github.com/ubclaunchpad/sleuth/wiki/Schemas
        '''
        if isinstance(item, ScrapyGenericPage):
            self.__process_generic_page(item)
        elif isinstance(item, ScrapyCourseItem):
            self.__process_course_item(item)
        elif isinstance(item, ScrapyRedditPost):
            self.__process_reddit_post(item)

        return item

    def __process_generic_page(self, item):
        '''
        Convert Scrapy item to Solr GenericPage and commit it to database
        Schema specified by sleuth_backend.solr.models.GenericPage
        '''
        solr_doc = GenericPage(
            id=item["url"],
            type="genericPage",
            name=item["title"],
            siteName=item["site_title"],
            updatedAt=self.__make_date(),
            content=self.__parse_content(item["raw_content"]),
            description=item["description"],
            links=item["links"]
        )
        solr_doc.save_to_solr(self.solr_connection)

    def __process_course_item(self, item):
        '''
        Convert Scrapy item to Solr CourseItem and commit it to database
        '''
        subject = item['subject']
        solr_doc = CourseItem(
            id=item['url'],
            type='courseItem',
            name=item['name'],
            updatedAt=self.__make_date(),
            description=item['description'],
            subjectId=subject['url'],
            subjectName=subject['name'],
            faculty=subject['faculty']
        )
        solr_doc.save_to_solr(self.solr_connection)

    def __process_reddit_post(self, item):
        '''
        Convert Scrapy item to Solr ReddiPost and commit it to database
        '''
        solr_doc = RedditPost(
            id=item['url'],
            type='redditPost',
            name=item['title'],
            updatedAt=self.__make_date(),
            description=item['post_content'],
            comments=item['comments'],
            links=item['links'],
        )
        solr_doc.save_to_solr(self.solr_connection)

    def __make_date(self):
        """
        Make a UTC date string in format 'Y-m-d H:M:S'
        """
        stamp = time.time()
        style = '%Y-%m-%d %H:%M:%S'
        return datetime.datetime.fromtimestamp(stamp).strftime(style)

    def __parse_content(self, raw_content):
        """
        Parse content list into single string
        TODO: make smarter
        """
        data = ' '.join(raw_content)
        return data
