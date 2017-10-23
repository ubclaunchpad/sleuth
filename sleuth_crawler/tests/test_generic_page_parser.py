from django.test import TestCase
from sleuth_crawler.tests.mocks import mock_response
from sleuth_crawler.scraper.scraper.items import ScrapyGenericPage
from sleuth_crawler.scraper.scraper.spiders.parsers import generic_page_parser as parser
import re

class TestGenericPageParser(TestCase):
    """
    Test GenericPageParser
    parsers.generic_page_parser
    """

    def test_parse_generic_item(self):
        """
        Test single item parse
        """
        response = mock_response('/test_data/ubc.txt', 'http://www.ubc.ca')
        children = ['http://www.google.com', 'http://www.reddit.com']
        item = parser.parse_generic_item(response, children)
        item = ScrapyGenericPage(item)
        self.assertEqual(item['url'], "http://www.ubc.ca")
        self.assertTrue(len(item['raw_content']) > 0)
        self.assertTrue(len(item['children']) > 0)
        self.assertEqual(item['description'], "The University of British Columbia is a global centre for research and teaching, consistently ranked among the top 20 public universities in the world.")
        self.assertEqual(item['children'], children)

        # Check that there are no HTML tags, no blank lines, no JavaScript
        html_regexp = re.compile(r'<[^>]*?>')
        js_regexp = re.compile(r'{[^*]*?}')
        for line in item['raw_content']:
            self.assertTrue(len(line) > 0)
            self.assertFalse(html_regexp.search(line))
            self.assertFalse(js_regexp.search(line))
