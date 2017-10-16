import pysolr
import json
from django.test import TestCase
from unittest.mock import MagicMock, patch
from sleuth_backend.solr.connection import SolrConnection
from sleuth_backend.solr.models import GenericPage

class MockAdmin(object):
        
    def __init__(self):
        pass

    def status(self):
        return json.dumps({
            "status": {
                "core1": "a core",
                "genericPage": "another core"
            }
        })

    def _get_url(self, url):
        return json.dumps({
            "schema": {
                "url": url
            }
        })

class MockSolr(object):
    
    def __init__(self):
        pass

    def add(self, docs):
        return docs

class TestSolrConnection(TestCase):

    @patch('pysolr.Solr')
    @patch('pysolr.SolrCoreAdmin')
    def test_fetch_core_names(self, admin_mock, solr_mock):
        solr_mock.return_value = MockSolr()
        admin_mock.return_value = MockAdmin()
        solr_connection = SolrConnection("http://a.test.url/solr")
        
        self.assertEqual(["core1", "genericPage"], solr_connection.core_names())
        self.assertEqual(["core1", "genericPage"], solr_connection.fetch_core_names())
        self.assertEqual("http://a.test.url/solr", solr_connection.url)
        
        for (_, value) in solr_connection.cores.items():
            self.assertIsInstance(value, MockSolr)

    @patch('pysolr.Solr')
    @patch('pysolr.SolrCoreAdmin')
    def test_fetch_core_schema(self, admin_mock, solr_mock):
        solr_mock.return_value = MockSolr()
        admin_mock.return_value = MockAdmin()
        solr_connection = SolrConnection("http://a.test.url/solr")
        expected_schema = {"url": "http://a.test.url/solr/test/schema"}
        self.assertEqual(expected_schema, solr_connection.fetch_core_schema("test"))

    @patch('pysolr.Solr')
    @patch('pysolr.SolrCoreAdmin')
    def test_insert_document(self, admin_mock, solr_mock):
        solr_mock.return_value = MockSolr()
        admin_mock.return_value = MockAdmin()
        solr_connection = SolrConnection("http://a.test.url/solr")
        solr_connection.cores["generic_page"] = MockSolr()
        doc = {"id": "testid"}
        response = solr_connection.insert_document("genericPage", doc)
        self.assertEqual([doc], response)

    def test_search(self):
        # TODO once search is properly done
        pass