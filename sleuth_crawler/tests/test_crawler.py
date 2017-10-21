from django.test import TestCase
from sleuth_crawler.tests.mocks import mock_response
from sleuth_crawler.scraper.scraper.spiders.broad_crawler import *
from sleuth_crawler.scraper.scraper.items import *
import re

class TestUbcBroadCralwer(TestCase):
    """
    Test UbcBroadCrawler
    ubc_homepage_spider.py
    """
    def setUp(self):
        self.spider = BroadCrawler()

    def test_parse_item(self):
        """
        Test single item parse
        """
        response = mock_response('/test_data/ubc.txt', 'http://www.ubc.ca')
        item = self.spider.parse_generic_item(response)
        item = ScrapyGenericPage(item)
        self.assertEqual(item['url'], "http://www.ubc.ca")
        self.assertTrue(len(item['raw_content']) > 0)
        self.assertTrue(len(item['children']) > 0)
        self.assertEqual(item['description'], "The University of British Columbia is a global centre for research and teaching, consistently ranked among the top 20 public universities in the world.")

        # Check that there are no HTML tags and no blank lines
        regexp = re.compile(r'<[^>]*?>')
        for line in item['raw_content']:
            self.assertTrue(len(line) > 0)
            self.assertFalse(regexp.search(line))
