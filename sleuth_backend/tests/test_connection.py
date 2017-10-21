import pdb
import pysolr
import json
import requests
from django.test import TestCase
from unittest.mock import MagicMock, patch
from sleuth_backend.solr.connection import SolrConnection
from sleuth_backend.solr.models import GenericPage

class MockAdmin(object):

    def __init__(self, status_response=None, get_url_response=None):
        self.status_response = status_response
        self.get_url_response = get_url_response

    def status(self):
        if self.status_response is not None:
            return json.dumps(self.status_response)
        return None

    def _get_url(self, url):
        if self.get_url_response is not None:
            return json.dumps(self.get_url_response)
        return None

class MockSolr(object):

    def __init__(self):
        pass

    def add(self, docs):
        return docs

class MockResponse(object):

    def __init__(self, content):
        self.content = content

class TestSolrConnection(TestCase):

    def create_instance(self, admin_mock, solr_mock):
        status_response = {
            "status": {
                "core1": "a core",
                "genericPage": "another core"
            }
        }
        url = "http://a.test.url/solr"
        get_url_response = {
            "schema": {
                "url": url
            }
        }
        solr_mock.return_value = MockSolr()
        admin_mock.return_value = MockAdmin(status_response, get_url_response)
        return SolrConnection(url)

    @patch('pysolr.Solr')
    @patch('pysolr.SolrCoreAdmin')
    def test_fetch_core_names(self, admin_mock, solr_mock):
        solr_connection = self.create_instance(admin_mock, solr_mock)

        self.assertEqual(["core1", "genericPage"], solr_connection.core_names())
        self.assertEqual(["core1", "genericPage"], solr_connection.fetch_core_names())
        self.assertEqual("http://a.test.url/solr", solr_connection.url)

        for (_, value) in solr_connection.cores.items():
            self.assertIsInstance(value, MockSolr)

    @patch('requests.get')
    @patch('pysolr.Solr')
    @patch('pysolr.SolrCoreAdmin')
    def test_fetch_core_schema(self, admin_mock, solr_mock, get_mock):
        solr_connection = self.create_instance(admin_mock, solr_mock)
        expected_response = {
            "schema" : {
                "url": "http://a.test.url/solr/test/schema"
            }
        }
        get_mock.return_value = MockResponse(json.dumps(expected_response))
        self.assertEqual(expected_response["schema"], solr_connection.fetch_core_schema("test"))

    @patch('pysolr.Solr')
    @patch('pysolr.SolrCoreAdmin')
    def test_insert_document(self, admin_mock, solr_mock):
        solr_connection = self.create_instance(admin_mock, solr_mock)
        solr_connection.cores["genericPage"] = MockSolr()
        doc = {"id": "testid"}
        response = solr_connection.insert_document("genericPage", doc)
        self.assertEqual([doc], response)

    @patch('pysolr.Solr')
    @patch('pysolr.SolrCoreAdmin')
    def test_optimize(self, admin_mock, solr_mock):
        solr_mock.return_value = MagicMock()
        admin_mock.return_value = MockAdmin()
        solr_connection = SolrConnection("http://a.test.url/solr")
        solr_connection.cores["generic_page"] = MagicMock()
        solr_connection.cores["c1"] = MagicMock()
        solr_connection.cores["c2"] = MagicMock()
        
        solr_connection.optimize("generic_page")
        self.assertTrue(solr_connection.cores["generic_page"].optimize.called)

        solr_connection.optimize()
        self.assertTrue(solr_connection.cores["generic_page"].optimize.called)
        self.assertTrue(solr_connection.cores["c1"].optimize.called)
        self.assertTrue(solr_connection.cores["c2"].optimize.called)

    @patch('requests.get')
    @patch('pysolr.Solr')
    @patch('pysolr.SolrCoreAdmin')
    def test_query(self, admin_mock, solr_mock, get_mock):
        response_content = {
            "response": {
                "numFound": 1,
                "start": 0,
                "docs": [
                    {
                        "id": "test",
                        "content": ["Some example content"]
                    }
                ]
            },
            "highlighting": {
                "test": {
                    "content": ["Some example content"]
                }
            }
        }
        solr_connection = self.create_instance(admin_mock, solr_mock)
        get_mock.return_value = MockResponse(json.dumps(response_content))

        result = solr_connection.query('genericPage', 'test', sort="updatedAt desc",
            start=5, rows=10, default_field="content", search_fields="content id",
            highlight_fields="content")
        self.assertEqual(json.dumps(response_content), result)
