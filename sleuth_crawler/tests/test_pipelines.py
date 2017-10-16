from django.test import TestCase
from unittest.mock import MagicMock, patch
from sleuth_crawler.scraper.scraper.pipelines import *

class TestSolrPipeline(TestCase):
    """
    Test Solr Pipeline
    ubc_homepage_spider.py
    TODO: prevent unintentional Solr coverage
    """
    @patch('sleuth_backend.solr.connection.SolrConnection')
    def setUp(self, fake_solr):
        self.fake_solr = fake_solr
        self.pipeline = SolrPipeline(fake_solr)

    def testProcessGenericPage(self):
        """
        Test Generic Page processing
        """
        item = ScrapyGenericPage()
        item["url"] = "http://www.ubc.ca"
        item["raw_content"] = "Ubc the best"
        self.pipeline.process_item(item)

        args = self.fake_solr.insert_document.call_args[0]
        self.assertTrue(args[0])
        self.assertTrue(args[1])
        doc_type = args[0]
        doc = args[1]
        self.assertEqual("genericPage", doc_type)
        self.assertEqual("http://www.ubc.ca", doc["id"])
        self.assertEqual("Ubc the best", doc["content"])
        self.assertTrue(doc["updatedAt"])
        print("Timestamp: " + doc["updatedAt"])
