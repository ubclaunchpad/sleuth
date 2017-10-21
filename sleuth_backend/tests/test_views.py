import json
from django.test import TestCase
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
        mock_query.return_value = json.dumps({
            "response": {
                "numFound": 1,
                "start": 0,
                "docs": [
                    {
                        "id": "www.cool.com",
                        "content": "Nice one dude",
                    }
                ]
            },
            "highlighting": {
                "www.cool.com": {
                    "content": ['Nice one dude']
                }
            }
        })
        params = {
            'q': 'somequery',
            'core': 'test',
        }
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        print('Response content is ' + str(result.content))
        response_body = json.loads(result.content)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(response_body, mock_query.return_value)
