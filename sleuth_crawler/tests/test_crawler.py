from django.test import TestCase
from unittest.mock import patch
from sleuth_crawler.tests.mocks import mock_response
from sleuth_crawler.scraper.scraper.spiders.broad_crawler import *
from sleuth_crawler.scraper.scraper.items import *

class TestBroadCralwer(TestCase):
    '''
    Test BroadCrawler
    spiders.broad_crawler
    '''

    def setUp(self):
        self.spider = BroadCrawler()

    @patch('sleuth_crawler.scraper.scraper.spiders.parsers.generic_page_parser.parse_generic_item')
    def test_parse_generic_item(self, fake_parser):
        '''
        Test crawler's redirect to generic_page_parser as default parser
        '''
        response = mock_response(file_name='/test_data/ubc.txt')
        self.spider.parse_generic_item(response)
        self.assertTrue(fake_parser.called)
        links_arg = fake_parser.call_args[0][1]
        self.assertTrue(len(links_arg)>0)
        self.assertFalse('http://www.ubc.ca' in links_arg)

    @patch('sleuth_crawler.scraper.scraper.spiders.parsers.reddit_parser.parse_post')
    def test_parse_reddit_post(self, fake_parser):
        '''
        Test crawler's redirect to reddit_parser
        '''
        response = mock_response(file_name='/test_data/reddit_text_post.txt')
        self.spider.parse_reddit_post(response)
        self.assertTrue(fake_parser.called)
        links_arg = fake_parser.call_args[0][1]
        self.assertTrue(len(links_arg)>0)
