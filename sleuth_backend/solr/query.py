'''
Solr query assembling
'''

import nltk

class Query(object):
    """
    This object allows component-based building and manipulation of Solr query strings.
    See class for available query manipulations.

    Params:
        query_str  (str): the desired query
        as_phrase (bool): should this query be formatted as a phrase (default=True)
        escape    (bool): should special characters be escaped from the phrase (default=False)
        sanitize  (bool): should query be stripped of trivial words (default=False)

    Example Usage:
        my_query = Query(query_str)
        my_query.select_and(other_query)    # my_query AND other_query
        my_query.select_or(other_query)     # my_query OR other_query
        return str(my_query)                # return query string
    """

    def __init__(self, query_str, as_phrase=True, escape=False, sanitize=False):
        """
        Initialize a query
        """
        self.query_str = query_str

        if escape:
            self._escape_special_chars()

        if sanitize:
            self._sanitize()

        if as_phrase:
            self._as_phrase()

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

    def for_single_field(self, field):
        '''
        Apply given field to query
        '''
        self.query_str = '{}:{}'.format(field, self.query_str)

    def fuzz(self, factor):
        '''
        "Fuzzes" the query by a given factor where 0 <= factor <=2.
        Acts differently depending on whether the query is a phrase or not.
        For phrases, this factor determines how far about the words of a
        phrase can be found.
        For terms, this factor determines how many insertions/deletions will
        still return a match.
        '''
        if factor < 0 or factor > 2:
            raise ValueError('Factor must be between 0 and 2.')
        self.query_str = '{}~{}'.format(self.query_str, factor)

    def for_fields(self, fields):
        """
        Apply given fields to query
        """
        if type(fields) is not dict:
            raise ValueError('Fields must be a dict of field names and boost factors')
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

    def _as_phrase(self):
        """
        Format query as entire phrase, and optionally set proximity for
        words within the phrase.
        """
        self.query_str = '"{}"'.format(self.query_str)

    def _sanitize(self):
        '''
        Trim nonessential words such as 'and', 'or', 'for'
        Parts of Speech types:
        http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        '''
        tags_to_keep = [
            'NN', 'NNS', 'NNP', 'NNPS',       # noun types
            'VB', 'VBG', 'VBN', 'VBP', 'VBZ', # verb types
            'JJ', 'JJR', 'JJS',               # adjective types
            'RB', 'RBR', 'RBS',               # adverbs
        ]
        tokens = nltk.word_tokenize(self.query_str)
        tags = nltk.pos_tag(tokens)
        words_list = []
        for tag in tags:
            if tag[1] in tags_to_keep:
                words_list.append(tag[0])
        self.query_str = ' '.join(words_list)

    def _escape_special_chars(self):
        '''
        Escape special characters that interfere with Solr's query parser.
        Ideally only use on queries where as_phrase=False, since special
        characters in phrases do not upset Solr.
        '''
        special_chars = ['!', '(', ')', '{', '}', '[', ']', '^', '"', '~', '*', '?', ':', '|', '&']
        for c in special_chars:
            self.query_str = self.query_str.replace(c, '\\'+c)
