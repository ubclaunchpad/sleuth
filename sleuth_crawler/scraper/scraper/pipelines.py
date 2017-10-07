# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from sleuth_backend.solr_module.solr_module import add_item
from scraper.items import GenericPage

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
    def process_item(self, item, spider):
        if isinstance(item, GenericPage):
            solr_item = self.__process_generic_page__(item)
            add_item(solr_item)

        return item

    def __process_generic_page__(self, item):
        solr_item = {}
        solr_item["id"] = item["url"]
        solr_item["data"] = item["page_data"]
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


