from sleuth_backend.solr.query import Query
from django.test import TestCase
from unittest.mock import MagicMock

class TestQuery(TestCase):
    """
    Test the Solr query object
    """

    def test_init(self):
        """
        Test initializing a Query
        as_phrase and not as_phrase
        """
        query_str = "hello"
        query = Query(query_str)
        self.assertEqual('"hello"', str(query))

        query = Query(query_str, as_phrase=False)
        self.assertEqual('hello', str(query))

        query = Query('wow:wow()', escape=True)
        self.assertEqual('"wow\:wow\(\)"', str(query))

    def test_for_fields(self):
        """
        Test applying fields to a Query
        """
        fields = {'id':1, 'name':10}
        query = Query("hello bruno")
        query.for_fields(fields)
        self.assertEqual(
            '"hello bruno" OR id:("hello bruno")^1 OR name:("hello bruno")^10',
            str(query)
        )
        not_dict = "not clean"
        self.failUnlessRaises(ValueError, query.for_fields, not_dict)

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

    def test_for_single_field(self):
        '''
        Test applying a single field to a query
        '''
        query = Query("hello bruno")
        query.for_single_field('id')
        self.assertEqual('id:"hello bruno"', str(query))

    def test_fuzz(self):
        '''
        Test applying a fuzz factor to a query
        '''
        query = Query("hello bruno")
        query.fuzz(2)
        self.assertEqual('"hello bruno"~2', str(query))
        self.failUnlessRaises(ValueError, query.fuzz, 7)

    def test_sanitation(self):
        '''
        Test query init with sanitize=True
        '''
        query = Query("The quick brown fox jumped over 12 lazy dogs", sanitize=True)
        print(str(query))
