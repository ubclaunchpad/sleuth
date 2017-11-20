import pdb
import pysolr
import json
import requests
from django.test import TestCase
from unittest.mock import MagicMock, patch, call
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

    def json(self):
        return self.content

class TestSolrConnection(TestCase):

    @patch('pysolr.SolrCoreAdmin')
    @patch('pysolr.Solr')
    def setUp(self, fake_solr, fake_admin):
        self.solr_mock = fake_solr
        self.admin_mock = fake_admin
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
        self.admin_mock.return_value = MockAdmin(status_response, get_url_response)
        self.solr_connection = SolrConnection(url)

    def test_fetch_core_names(self):
        solr_connection = self.solr_connection
        self.solr_mock.return_value = MockSolr
        self.assertEqual(["core1", "genericPage"], solr_connection.core_names())
        self.assertEqual(["core1", "genericPage"], solr_connection.fetch_core_names())
        self.assertEqual("http://a.test.url/solr", solr_connection.url)

    @patch('requests.get')
    def test_fetch_core_schema(self, get_mock):
        solr_connection = self.solr_connection
        expected_response = {
            "schema" : {
                "url": "http://a.test.url/solr/test/schema"
            }
        }
        get_mock.return_value = MockResponse(expected_response)
        self.assertEqual(expected_response["schema"], solr_connection.fetch_core_schema("test"))

    def test_queue_document(self):
        solr_connection = self.solr_connection
        solr_connection.cores["genericPage"] = self.solr_mock
        doc = {"id": "testid"}
        response = solr_connection.queue_document("genericPage", doc)
        self.assertEqual(None, response)

        with self.assertRaises(ValueError):
            solr_connection.queue_document("blah", doc)

        # Test auto insertion past QUEUE_THRESHOLD
        response_docs = []
        for _ in range(solr_connection.QUEUE_THRESHOLD - 2):
            response = solr_connection.queue_document("genericPage", doc)
        solr_connection.queue_document("genericPage", doc)
        response_docs += solr_connection.QUEUE_THRESHOLD * [doc]
        self.assertEqual((response_docs,), self.solr_mock.add.call_args[0])

    def test_insert_documents(self):
        solr_connection = self.solr_connection
        solr_connection.cores["genericPage"] = self.solr_mock
        doc = {"id": "testid"}

        with self.assertRaises(ValueError):
            solr_connection.queue_document("blah", [doc])

        solr_connection.insert_documents("genericPage", [doc,doc])
        self.assertEqual(([doc,doc],), self.solr_mock.add.call_args[0])

    def test_insert_queued(self):
        solr_connection = self.solr_connection
        solr_connection.cores['genericPage'] = self.solr_mock
        solr_connection.cores['core1'] = self.solr_mock
        doc1 = {'id': 'testid'}
        doc2 = {'id': 'other_test_id'}

        solr_connection.queue_document('genericPage', doc1)
        solr_connection.queue_document('core1', doc2)
        solr_connection.insert_queued()
        self.assertEqual(2, self.solr_mock.add.call_count)
        self.assertEqual(
            [call([{'id': 'other_test_id'}]), call([{'id': 'testid'}])],
            self.solr_mock.add.call_args_list
        )

    def test_optimize(self):
        status_response = {
            "status": {
                "c1": True,
                "c2": True,
            }
        }
        self.admin_mock.return_value = MockAdmin(status_response=status_response)
        self.solr_connection.cores["generic_page"] = MagicMock()
        self.solr_connection.cores["c1"] = MagicMock()
        self.solr_connection.cores["c2"] = MagicMock()
        solr_connection = self.solr_connection

        self.solr_connection.optimize("generic_page")
        self.assertTrue(solr_connection.cores["generic_page"].optimize.called)

        self.solr_connection.optimize()
        self.assertTrue(solr_connection.cores["generic_page"].optimize.called)
        self.assertTrue(solr_connection.cores["c1"].optimize.called)
        self.assertTrue(solr_connection.cores["c2"].optimize.called)

    @patch('requests.get')
    def test_query(self, get_mock):
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
        solr_connection = self.solr_connection
        get_mock.return_value = MockResponse(response_content)

        result = solr_connection.query('genericPage', 'test', sort="updatedAt desc",
            start=5, rows=10, default_field="content", search_fields="content id",
            highlight_fields="content")
        self.assertEqual(response_content, result)
