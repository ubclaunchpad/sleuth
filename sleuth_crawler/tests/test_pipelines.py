from django.test import TestCase
from unittest.mock import MagicMock, patch
from sleuth_crawler.scraper.scraper.pipelines import *

class TestSolrPipeline(TestCase):
    '''
    Test Solr Pipeline
    ubc_homepage_spider.py
    '''
    
    @patch('sleuth_backend.solr.connection.SolrConnection')
    def setUp(self, fake_solr):
        self.fake_solr = fake_solr
        self.pipeline = SolrPipeline(fake_solr)

    def test_process_generic_page(self):
        '''
        Test Generic Page processing
        '''
        item = ScrapyGenericPage(
            url="http://www.ubc.ca",
            title="title",
            site_title="site title",
            description="",
            raw_content=["description1","description2"],
            links=["www.google.com","www.reddit.com"]
        )
        self.pipeline.process_item(item)

        args = self.__assert_and_return_args()
        doc_type = args[0]
        doc = args[1]
        self.assertEqual("genericPage", doc_type)
        self.assertEqual("http://www.ubc.ca", doc["id"])
        self.assertEqual("description1 description2", doc["content"])
        self.assertTrue(len(doc["links"])==2)
        self.assertTrue(doc["updatedAt"])
        self.assertEqual("title", doc["name"])
        self.assertEqual("site title", doc["siteName"])

    def test_process_course_item(self):
        '''
        Test Course Item processing
        '''
        item = ScrapyCourseItem(
            subject={"url":"some.url","name":"somename","faculty":"somefaculty"},
            url="subject.url",
            name="CPSC110 Trust the Natural Recursion",
            description="racket"
        )
        self.pipeline.process_item(item)
        args = self.__assert_and_return_args()
        doc_type = args[0]
        doc = args[1]
        self.assertEqual("courseItem", doc_type)
        self.assertEqual("subject.url", doc["id"])

    def test_process_reddit_post(self):
        '''
        Test Reddit Post processing
        '''
        item = ScrapyRedditPost(
            url='reddit.com/r/ubc', title='', subreddit='', post_content='',
            comments=['wow!'], links=[]
        )
        self.pipeline.process_item(item)
        args = self.__assert_and_return_args()
        doc_type = args[0]
        doc = args[1]
        self.assertEqual('redditPost', doc_type)
        self.assertEqual('wow!', doc['comments'][0])

    def test_close_spider(self):
        '''
        Test that closing spider calls solrConnection.optimize()
        '''
        self.pipeline.close_spider()
        self.assertTrue(self.fake_solr.optimize.called)

    def __assert_and_return_args(self):
        # Utility function for determining that queue_document
        # was called with two parameters and returning the arguments
        args = self.fake_solr.queue_document.call_args[0]
        self.assertTrue(args[0])
        self.assertTrue(args[1])
        doc_type = args[0]
        doc = args[1]
        return [doc_type, doc]
