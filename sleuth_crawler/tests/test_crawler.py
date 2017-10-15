from django.test import TestCase
from sleuth_crawler.tests.mocks import mock_response
from sleuth_crawler.scraper.scraper.spiders.ubc_homepage_spider import *

class TestUbcBroadCralwer(TestCase):
    """
    Test UbcBroadCrawler
    ubc_homepage_spider.py
    """
    def setUp(self):
        self.spider = UbcBroadCrawler()

    def test_parse_item(self):
        """
        Test single item parse
        """
        response = mock_response('/test_data/ubc.txt', 'http://www.ubc.ca')
        item = self.spider.parse_item(response)
        item = GenericPage(item)
        self.assertEqual(item['url'], "http://www.ubc.ca")
        self.assertTrue(len(item['raw_content']) > 0)
