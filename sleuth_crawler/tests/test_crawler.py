from django.test import TestCase
from unittest.mock import patch
from sleuth_crawler.tests.mocks import mock_response
from sleuth_crawler.scraper.scraper.spiders.broad_crawler import *
from sleuth_crawler.scraper.scraper.items import *
import re

class TestBroadCralwer(TestCase):
    """
    Test BroadCrawler
    spiders.broad_crawler
    """
    def setUp(self):
        self.spider = BroadCrawler()

    def test_request_filtering(self):
        """
        Test filtering normal requests
        """
        # Direct non-matching requests to default parser (GenericPage)
        req_in = scrapy.Request('https://www.ubc.ca')
        req = self.spider.process_req(req_in)
        self.assertTrue(req)
        self.assertFalse(req.callback)

    def test_request_filtering_course(self):
        """
        Test filtering course requests
        """
        # Redirect to parse_subjects if parent courses page
        req_pass = scrapy.Request('https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=0')
        req = self.spider.process_req(req_pass)
        self.assertEqual(req.callback.__name__, course_parser.parse_subjects.__name__)

        # Discard request if children courses page
        req_discard = scrapy.Request('https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=1&dept=ASTR')
        req = self.spider.process_req(req_discard)
        self.assertFalse(req)

    @patch('sleuth_crawler.scraper.scraper.spiders.parsers.generic_page_parser.parse_generic_item')
    def test_parse_generic_item(self, fake_parser):
        """
        Test crawler's redirect to generic_page_parser as default parser
        """
        response = mock_response(file_name='/test_data/ubc.txt')
        self.spider.parse_generic_item(response)
        self.assertTrue(fake_parser.called)
