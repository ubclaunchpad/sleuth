#import nltk

"""
Solr queries
"""

class Query(object):
    """
    This object allows component-based building and manipulation of Solr query strings.
    See class for available query manipulations.

    Params:
        query_str (str): the desired query
        as_phrase (str): should this query be formatted as a phrase (default=True)
        fields   (dict): the Solr fields to apply this query to (default=None) 
        proximity (int): proximity for parts of the search phrase (default=None)
                         only works if as_phrase=True

    Example Usage:
        my_query = Query(query_str)
        my_query.select_and(other_query)    # my_query AND other_query
        my_query.select_or(other_query)     # my_query OR other_query
        return str(my_query)                # return query string
    """

    def __init__(self, query_str, as_phrase=True, fields=None, proximity=None):
        """
        Initialize a query
        """
        self.query_str = query_str
        self._sanitize()

        if as_phrase:
            self._as_phrase(proximity)
        
        if fields:
            if type(fields) is not dict:
                raise ValueError('Fields must be a dict of field names and boost factors')
            self._for_fields(fields)

    def __str__(self):
        """
        Return query as a string
        """
        return self.query_str

    def boost_importance(self, factor):
        """
        Raise the immportance of this query to given factor
        """
        self.query_str = '({})^{}'.format(self.query_str, str(factor))

    def select_and(self, query):
        """
        Join this query and another query with an AND select
        """
        self.query_str = '{} AND {}'.format(self.query_str, str(query))

    def select_or(self, query):
        """
        Join this query and another query with an OR select
        """
        self.query_str = '{} OR {}'.format(self.query_str, str(query))

    def select_require(self, terms):
        """
        Make query require the given terms
        """
        for term in terms:
            self.query_str += '+{}'.format(term)
    
    def _for_fields(self, fields):
        """
        Apply given fields to query
        """
        self._for_fields_helper(self.query_str, list(fields.items()))

    def _for_fields_helper(self, query_str, fields):
        if not fields:
            return
    
        field, boost = fields[0]
        query = Query(query_str, as_phrase=False)
        query.boost_importance(boost)
        query = Query('{}:{}'.format(field, str(query)), as_phrase=False)
        self.select_or(query)
        self._for_fields_helper(query_str, fields[1:])

    def _as_phrase(self, proximity):
        """
        Format query as entire phrase, and optionally set proximity for
        words within the phrase.
        """
        self.query_str = '"{}"'.format(self.query_str)
        if proximity:
            self.query_str = '{}~{}'.format(self.query_str, proximity)

    def _sanitize(self):
        """
        Trim nonessential words such as 'and', 'or', 'for'
        """
        # TODO: trim useless words like 'and', 'or', 'for' 
        # from query if as_phrase is false using NLTK POS tagger
        self.query_str = ' '.join(self.query_str.split())
