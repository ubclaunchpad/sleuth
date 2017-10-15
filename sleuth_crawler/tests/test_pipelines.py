from django.test import TestCase
from unittest.mock import MagicMock
from sleuth_crawler.scraper.scraper.pipelines import *

class TestSolrPipeline(TestCase):
    """
    Test Solr Pipeline
    ubc_homepage_spider.py
    TODO: prevent unintentional Solr coverage
    """
    def setUp(self):
        self.pipeline = SolrPipeline()
        self.solr_add_item = solr.add_item
        solr.add_item = MagicMock()

    def tearDown(self):
        solr.add_item = self.solr_add_item

    def testProcessGenericPage(self):
        """
        Test Generic Page processing
        """
        item = GenericPage()
        item["url"] = "http://www.ubc.ca"
        item["raw_content"] = "Ubc the best"
        self.pipeline.process_item(item)

        args = solr.add_item.call_args[0]
        self.assertEqual("genericPage", args[1])
        self.assertEqual("http://www.ubc.ca", args[0]["id"])
        self.assertEqual("Ubc the best", args[0]["data"]["content"])
        self.assertTrue(args[0]["data"]["dateUpdated"])
        print("Timestamp: " + args[0]["data"]["dateUpdated"])
