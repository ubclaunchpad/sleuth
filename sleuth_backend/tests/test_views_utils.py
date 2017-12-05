import sleuth_backend.views.views_utils as utils
from django.test import TestCase

class TestViewsUtils(TestCase):
    '''
    Test views utility functions
    '''

    def test_build_core_request(self):
        '''
        Test building list of requested cores
        '''
        solr_cores = ['genericPage', 'redditPost', 'courseItem']

        # one requested core
        result = utils.build_core_request('genericPage', solr_cores)
        self.assertEquals(['genericPage'], result)

        # multiple requested cores
        result = utils.build_core_request('genericPage,redditPost', solr_cores)
        self.assertEquals(['genericPage', 'redditPost'], result)

        # some invalid cores
        with self.assertRaises(ValueError):
            utils.build_core_request('wow,redditPost', solr_cores)

        # all cores invalid
        with self.assertRaises(ValueError):
            utils.build_core_request('geasdficPage,redasdf', solr_cores)

        # no given cores
        result = utils.build_core_request('', solr_cores)
        self.assertEquals(solr_cores, result)

    def test_build_return_fields(self):
        '''
        Test building string of return fields
        '''
        result = utils.build_return_fields('')
        self.assertEquals('id,updatedAt,name,description', result)

        with self.assertRaises(ValueError):
            utils.build_return_fields('asdfasdf')

        with self.assertRaises(ValueError):
            utils.build_return_fields('links,sadf')
