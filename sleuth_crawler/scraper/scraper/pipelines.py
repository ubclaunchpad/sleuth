# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, time, datetime
from sleuth_backend.views.views import SOLR
from sleuth_backend.solr.models import *
from sleuth_crawler.scraper.scraper.items import *

class JsonLogPipeline(object):
    """
    Log spider output to JSON file
    """
    def open_spider(self, spider):
        self.file = open("log.json", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class SolrPipeline(object):
    """
    Process item and store in Solr
    """
    def __init__(self, solr_connection=SOLR):
        self.solr_connection = solr_connection

    def process_item(self, item):
        """
        Match item type to predefined Schemas
        https://github.com/ubclaunchpad/sleuth/wiki/Schemas
        """
        if isinstance(item, ScrapyGenericPage):
            solr_doc = self.__process_generic_page__(item)
            solr_doc.save_to_solr(self.solr_connection)

        return item

    def __process_generic_page__(self, item):
        """
        Convert Scrapy item to Solr GenericPage
        """
        stamp = time.time()
        style = '%Y-%m-%d %H:%M:%S'
        solr_doc = GenericPage(
            id=item["url"],
            type="genericPage",
            updatedAt=datetime.datetime.fromtimestamp(stamp).strftime(style),
            content=item["raw_content"]
        )
        return solr_doc


class CourseToDjangoPipeline(object):
    """
    Saves course data to Django
    """
    def open_spider(self, spider):
        return
    
    def close_spider(self, spider):
        return

    def process_item(self, item, spider):
        return


