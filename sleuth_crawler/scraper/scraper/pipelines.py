# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, time, datetime
import sleuth_backend.solr.solr as solr
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
    def process_item(self, item):
        """
        Match item type to predefined Schemas
        https://github.com/ubclaunchpad/sleuth/wiki/Schemas
        """
        if isinstance(item, GenericPage):
            solr_item = self.__process_generic_page__(item)
            solr.add_item(solr_item, solr_item["type"])

        return item

    def __process_generic_page__(self, item):
        """
        Convert item to Generic Page
        {
            "id": "http://www.ubc.ca/about",
            "type": "genericPage",
            "siteName": "UBC",
            "keywords": ["keyword1", "keyword2"],
            "data": {
                "dateUpdated": "%Y-%m-%d %H:%M:%S", // UTC timestamp
                "pageName": "About",
                "pageTitle": "About UBC",
                "content": "UBC is a great place..."
            }
        }
        TODO: handle currently missing datafields
        TODO: improve "content"
        """
        stamp = time.time()
        style = '%Y-%m-%d %H:%M:%S'
        solr_item = {
            "id": item["url"],
            "type": "genericPage",
            "siteName": "",
            "keywords": [],
            "data": {
                "dateUpdated": datetime.datetime.fromtimestamp(stamp).strftime(style),
                "pageName": "",
                "pageTitle": "",
                "content": item["raw_content"]
            }
        }
        return solr_item


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


