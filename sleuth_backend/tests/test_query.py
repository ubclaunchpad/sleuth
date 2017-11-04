from sleuth_backend.solr.query import Query
from django.test import TestCase
from unittest.mock import MagicMock

class TestQuery(TestCase):
    """
    Test the Solr query object
    """

    def test_basic_init(self):
        """
        Test initializing a Query
        as_phrase and not as_phrase
        with and without proximity parameter
        """
        query_str = "hello"
        query = Query(query_str)
        self.assertEqual('"hello"', str(query))

        query = Query(query_str, proximity=5)
        self.assertEqual('"hello"~5', str(query))

        query = Query(query_str, as_phrase=False)
        self.assertEqual('hello', str(query))

    def test_init_fields(self):
        """
        Test initializing a Query with fields applied
        """
        query_str = "hello bruno"
        fields = {'id':1, 'name':10}
        query = Query(query_str, fields=fields)
        self.assertEqual(
            '"hello bruno" OR id:("hello bruno")^1 OR name:("hello bruno")^10',
            str(query)
        )
        not_dict = "not clean"
        self.failUnlessRaises(ValueError, Query, query_str, fields=not_dict)

    def test_boost_importance(self):
        """
        Test boosting the importance of a query
        """
        query_str = "hello bruno"
        query = Query(query_str)
        query.boost_importance(5)
        self.assertEqual('("hello bruno")^5', str(query))

    def test_selects(self):
        """
        Test select operators: AND, OR, REQUIRE
        """
        # AND
        query1 = Query("hello bruno")
        query2 = Query("bye bruno")
        query1.select_and(query2)
        self.assertEqual('"hello bruno" AND "bye bruno"', str(query1))

        # OR
        query1 = Query("hello bruno")
        query1.select_or(query2)
        self.assertEqual('"hello bruno" OR "bye bruno"', str(query1))

        # REQUIRE
        query1 = Query("hello bruno")
        terms = ["hack", "wack"]
        query1.select_require(terms)
        self.assertEqual('"hello bruno"+hack+wack', str(query1))
