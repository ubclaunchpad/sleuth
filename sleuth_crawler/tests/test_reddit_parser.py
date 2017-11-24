from django.test import TestCase
from sleuth_crawler.tests.mocks import mock_response
from sleuth_crawler.scraper.scraper.items import ScrapyRedditPost
from sleuth_crawler.scraper.scraper.spiders.parsers import reddit_parser as parser
import re

class TestGenericPageParser(TestCase):
    '''
    Tests the reddit post parser
    parsers.reddit_parser
    '''

    def test_parse_text_post(self):
        '''
        Test parsing a reddit text post
        '''
        response = mock_response('/test_data/reddit_text_post.txt', 'http://www.reddit.com/')
        links = ['http://www.google.com', 'http://www.reddit.com']
        item = parser.parse_post(response, links)
        item = ScrapyRedditPost(item)
        self.assertEqual('UBC', item['subreddit'])
        self.assertEqual(
            "As a first year student it's really hard to get into the UBC discord",
            item['title']
        )
        self.assertEqual(
            "Don't worry, it feels like that for everyone.At some point, the UBC discord became it's own little circle-jerk of friends, exclusive to anyone else. There are about 8-10 regular users, who communicate mainly through inside jokes and 4chan-esque internet humor. You're better off without them, I guarantee.",
            item['comments'][0]
        )

    def test_karma_fail(self):
        '''
        Test if the parser discards low-karma or no-karma posts
        '''
        response = mock_response()
        item = parser.parse_post(response, [])
        self.assertFalse(item)
