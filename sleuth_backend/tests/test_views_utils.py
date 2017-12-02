import sleuth_backend.views.views_utils as utils
from django.test import TestCase

class TestViewsUtils(TestCase):

    def test_build_core_request(self):
        solr_cores = ['genericPage', 'redditPost', 'courseItem']

        # one requested core
        result = utils.build_core_request('genericPage', solr_cores)
        self.assertEquals(['genericPage'], result)        

        # multiple requested cores
        result = utils.build_core_request('genericPage,redditPost', solr_cores)
        self.assertEquals(['genericPage', 'redditPost'], result)

        # some invalid cores
        result = utils.build_core_request('wow,redditPost', solr_cores)
        self.assertEquals(['redditPost'], result)

        # all cores invalid
        result = utils.build_core_request('geasdficPage,redasdf', solr_cores)
        self.assertEquals(solr_cores, result)

        # no given cores
        result = utils.build_core_request('', solr_cores)
        self.assertEquals(solr_cores, result)

    def test_build_return_fields(self):
        result = utils.build_return_fields('')
        self.assertEquals('id,updatedAt,name,description', result)

        result = utils.build_return_fields('asdfasdf')
        self.assertEquals('id,updatedAt,name,description', result)

        result = utils.build_return_fields('links,sadf')
        self.assertEquals('id,updatedAt,name,description,links', result)

        result = utils.build_return_fields('asdf,links,subreddit')
        self.assertEquals('id,updatedAt,name,description,links,subreddit', result)
