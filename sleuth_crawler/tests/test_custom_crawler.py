from django.test import TestCase
from sleuth_crawler.scraper.scraper.spiders.custom_crawler import *

class TestCustomCrawler(TestCase):
    '''
    Test custom crawler
    spiders.custom_crawler
    '''

    def test_setup(self):
        spider = CustomCrawler(['www.url.com'], self.test_setup)
        self.assertEqual(spider.parse.__name__, 'test_setup')
        self.assertEqual(spider.start_urls, ['www.url.com'])
