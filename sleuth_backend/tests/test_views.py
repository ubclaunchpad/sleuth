import json
import pysolr
from django.test import TestCase
from django.http import HttpResponse
from unittest.mock import MagicMock, patch
from sleuth_backend.views.views import cores, search, getdocument

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
    def test_cores_with_get(self, mock_core_names):
        mock_core_names.return_value = ['core1', 'core2']
        mock_request = MockRequest('GET')
        result = cores(mock_request)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, b'["core1", "core2"]')

    @patch('sleuth_backend.solr.connection.SolrConnection.query')
    def test_apis_without_get(self, mock_query):
        mock_query.return_value = {}
        mock_request = MockRequest('POST')
        result = search(mock_request)
        self.assertEqual(result.status_code, 405)
        result = getdocument(mock_request)
        self.assertEqual(result.status_code, 405)

    @patch('sleuth_backend.solr.connection.SolrConnection.query')
    def test_apis_without_params(self, mock_query):
        mock_query.return_value = {}
        mock_request = MockRequest('GET', get=MockGet({}))
        result = search(mock_request)
        response_body = json.loads(result.content)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(response_body['errorType'], 'INVALID_SEARCH_REQUEST')
        result = getdocument(mock_request)
        response_body = json.loads(result.content)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(response_body['errorType'], 'INVALID_GETDOCUMENT_REQUEST')

    @patch('sleuth_backend.solr.connection.SolrConnection.core_names')
    @patch('sleuth_backend.solr.connection.SolrConnection.query')
    def test_apis_with_valid_request(self, mock_query, mock_cores):
        mock_cores.return_value = ['genericPage', 'redditPost', 'courseItem']

        # genericPage search
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
            'type': 'genericPage',
            'return': 'content'
        }
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        self.assertEqual(result.status_code, 200)
        mock_response = mock_query.return_value
        mock_response['response']['docs'][0]['id'] = 'www.cool.com'
        mock_response['response']['docs'][0]['updatedAt'] = ''
        mock_response['response']['docs'][0]['name'] = ''
        mock_response['response']['docs'][0]['description'] = 'Nice one dude'
        self.maxDiff = None
        self.assertEqual(
            json.loads(result.content.decode('utf-8')),
            {
                "data": [{"type": "genericPage", "response": {"numFound": 1, "start": 0, "docs": [{"id": "www.cool.com", "description": "Nice one dude", "updatedAt": "", "name": "", "content": ""}]},
                          "highlighting": {"www.cool.com": {"content": ["Nice one dude"]}}}],
                "request": {"query": "somequery", "types": ["genericPage"], "return_fields": ["id", "updatedAt", "name", "description", "content"], "state": ""}
            }
        )

        # multicore search
        mock_cores.return_value = ['courseItem', 'courseItem']
        params = { 'q': 'somequery' }
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            json.loads(result.content.decode('utf-8')), 
            {'data': [{'type': 'courseItem', 'response': {'numFound': 1, 'start': 0, 'docs': [{'id': 'www.cool.com', 'description': 'Nice one dude', 'updatedAt': '', 'name': '', 'content': ''}]}, 'highlighting': {'www.cool.com': {'content': ['Nice one dude']}}}, {'type': 'courseItem', 'response': {'numFound': 1, 'start': 0, 'docs': [
            {'id': 'www.cool.com', 'description': 'Nice one dude', 'updatedAt': '', 'name': '', 'content': ''}]}, 'highlighting': {'www.cool.com': {'content': ['Nice one dude']}}}], 'request': {'query': 'somequery', 'types': ['courseItem', 'courseItem'], 'return_fields': ['id', 'updatedAt', 'name', 'description'], 'state': ''}}
        )

        # redditPost search
        mock_cores.return_value = ['genericPage', 'redditPost', 'courseItem']
        mock_query.return_value['type'] = 'redditPost'
        mock_query.return_value['highlighting']['www.cool.com'] = {'content': ['Nice']}
        params = { 'q': 'somequery', 'type': 'redditPost' }
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        self.assertEqual(result.status_code, 200)
        mock_response = mock_query.return_value
        
        # getdocument       
        params = {
            'id': 'somequery',
            'type': 'genericPage',
            'return': 'content'
        }
        mock_request = MockRequest('GET', get=MockGet(params))
        result = getdocument(mock_request)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            json.loads(result.content.decode('utf-8')),
            {'data': {'type': 'genericPage', 'doc': {'id': 'www.cool.com', 'description': 'Nice one dude', 'updatedAt': '', 'name': '', 'content': ''}}, 'request': {
            'query': 'somequery', 'types': ['genericPage'], 'return_fields': ['id', 'updatedAt', 'name', 'description', 'content'], 'state': ''}}
        )

        mock_query.return_value['response']['numFound'] = 0
        mock_request = MockRequest('GET', get=MockGet(params))
        result = getdocument(mock_request)
        self.assertEqual(result.status_code, 404)

    @patch('sleuth_backend.solr.connection.SolrConnection.core_names')
    @patch('sleuth_backend.solr.connection.SolrConnection.query')
    def test_apis_with_error_response(self, mock_query, mock_cores):
        mock_cores.return_value = ['test']        

        # Solr response error
        mock_query.return_value = {
            "error": {
                "msg": "org.apache.solr.search.SyntaxError",
                "code": 400,
            }
        }
        params = {
            'q': 'somequery',
            'type': 'test',
        }
        expected_response = json.dumps({
            "message": "org.apache.solr.search.SyntaxError on core test",
            "errorType": "SOLR_SEARCH_ERROR",
        })
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.content.decode("utf-8"), expected_response)
        mock_request = MockRequest('GET', get=MockGet({'id':'query', 'type': 'test'}))
        result = getdocument(mock_request)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.content.decode("utf-8"), expected_response)

        # pysolr error
        mock_query.side_effect = pysolr.SolrError()
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        self.assertEqual(result.status_code, 400)
        mock_request = MockRequest('GET', get=MockGet({'id':'query'}))
        result = getdocument(mock_request)
        self.assertEqual(result.status_code, 400)

        # Key error
        mock_query.side_effect = KeyError()
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        self.assertEqual(result.status_code, 500)
        mock_request = MockRequest('GET', get=MockGet({'id':'query'}))
        result = getdocument(mock_request)
        self.assertEqual(result.status_code, 500)

        # Value error
        mock_query.side_effect = ValueError()
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        self.assertEqual(result.status_code, 500)
        mock_request = MockRequest('GET', get=MockGet({'id':'query'}))
        result = getdocument(mock_request)
        self.assertEqual(result.status_code, 500)

        # Invalid param error
        params = {
            'q': 'somequery',
            'type': 'asdlialisfas',
        }
        mock_request = MockRequest('GET', get=MockGet(params))
        result = search(mock_request)
        self.assertEqual(result.status_code, 400)
        mock_request = MockRequest('GET', get=MockGet({'id':'query','type':'asdf'}))
        result = getdocument(mock_request)
        self.assertEqual(result.status_code, 400)
