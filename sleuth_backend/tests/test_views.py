import json
import pysolr
from django.test import TestCase
from django.http import HttpResponse
from unittest.mock import MagicMock, patch
from sleuth_backend.views.views import cores, search

class MockGet(object):

    def __init__(self, params):
        self.params = params

    def get(self, param, default):
        return self.params[param] if param in self.params else default

class MockRequest(object):

    def __init__(self, method, get=None):
        self.method = method
        if get is not None:
            self.GET = get

class TestAPI(TestCase):

    @patch('sleuth_backend.solr.connection.SolrConnection.core_names')
    def test_cores_without_get(self, mock_core_names):
        mock_core_names.return_value = ['core1', 'core2']
        mock_request = MockRequest('POST')
        result = cores(mock_request)
        self.assertEqual(result.status_code, 405)

    @patch('sleuth_backend.solr.connection.SolrConnection.core_names')
    def test_cores_without_get(self, mock_core_names):
        mock_core_names.return_value = ['core1', 'core2']
        mock_request = MockRequest('GET')
        result = cores(mock_request)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, b'["core1", "core2"]')

    @patch('sleuth_backend.solr.connection.SolrConnection.query')
    def test_search_without_get(self, mock_query):
        mock_query.return_value = {}
        mock_request = MockRequest('POST')
        result = search(mock_request)
        self.assertEqual(result.status_code, 405)

    @patch('sleuth_backend.solr.connection.SolrConnection.query')
    def test_search_without_params(self, mock_query):
        mock_query.return_value = {}
        mock_request = MockRequest('GET', get=MockGet({}))
        result = search(mock_request)
        response_body = json.loads(result.content)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(response_body['errorType'], 'INVALID_SEARCH_REQUEST')

    @patch('sleuth_backend.solr.connection.SolrConnection.query')
    def test_search_with_valid_request(self, mock_query):
        mock_query.return_value = {
            "type": "genericPage",
            "response": {
                "numFound": 1,
                "start": 0,
                "docs": [
                    {
                        "id": ["www.cool.com"],
                        "description": ["Nice one dude"],
                    }
                ]
            },
            "highlighting": {
                "www.cool.com": {
                    "content": ['Nice one dude']
                }
            }
        }
        params = {
            'q': 'somequery',
            'core': 'test',
            'return': 'content'
        }
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        self.assertEqual(result.status_code, 200)

        mock_query['response']['docs']['id'] = mock_query['response']['docs']['id'][0]
        mock_query['response']['docs']['description'] = mock_query['response']['docs']['description'][0]
        self.assertEqual(
            result.content.decode("utf-8"), 
            str({
                'data':[mock_query.return_value],
                'request':{
                    'query':'somequery','types':['test'],
                    'return_fields':['id','updatedAt','name','description','content'],
                    'state':''
                }
            })
        )

    @patch('sleuth_backend.solr.connection.SolrConnection.core_names')
    @patch('sleuth_backend.solr.connection.SolrConnection.query')
    def test_search_multicore(self, mock_query, mock_cores):
        mock_query.return_value = {
            "type": "courseItem",
            "response": {
                "numFound": 1,
                "start": 0,
                "docs": [
                    {
                        "id": ["www.cool.com"],
                        "description": ["Nice one dude"],
                    }
                ]
            },
            "highlighting": {
                "www.cool.com": {
                    "content": ['Nice one dude']
                }
            }
        }
        mock_cores.return_value = ['courseItem', 'courseItem']
        params = { 'q': 'somequery' }
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        self.assertEqual(result.status_code, 200)

        mock_query['response']['docs']['id'] = mock_query['response']['docs']['id'][0]
        mock_query['response']['docs']['description'] = mock_query['response']['docs']['description'][0]
        self.assertEqual(
            result.content.decode("utf-8"), 
            str({
                'data':[mock_query.return_value, mock_query.return_value],
                'request':{
                    'query':'somequery','types':['courseItem','courseItem'],
                    'return_fields':['id','updatedAt','name','description'],
                    'state':''
                }
            })
        )

    @patch('sleuth_backend.solr.connection.SolrConnection.query')
    def test_search_with_error_response(self, mock_query):
        mock_query.return_value = {
            "error": {
                "msg": "org.apache.solr.search.SyntaxError",
                "code": 400,
            }
        }
        params = {
            'q': 'somequery',
            'core': 'test',
        }
        expected_response = json.dumps({
            "message": "org.apache.solr.search.SyntaxError on core test",
            "errorType": "SOLR_SEARCH_ERROR",
        })
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.content.decode("utf-8"), expected_response)
