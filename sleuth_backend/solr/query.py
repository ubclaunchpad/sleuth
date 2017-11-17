'''
Solr query assembling
'''

import nltk

class Query(object):
    '''
    This object allows component-based building and manipulation of Solr query strings.
    See class for available query manipulations.

    Params:
        query_str  (str): the desired query
        as_phrase (bool): should this query be formatted as a phrase (default=True)
        escape    (bool): should special characters be escaped from the phrase (default=False)
        sanitize  (bool): should query be stripped of trivial words (default=False)

    Example Usage:
        query = Query(doc_id, as_phrase=False, escape=True) \
            .for_single_field('id') \
            .select_or(
                Query(doc_id + '/', as_phrase=False, escape=True) \
                .for_single_field('id') \
                .select_or(query_variation)
            )
        
        query = Query(doc_id, as_phrase=False, escape=True).for_single_field('id')
        query_variation = Query(doc_id + '/', as_phrase=False, escape=True) \
            .for_single_field('id') \
            .select_or(query_variation)
        combination = query.select_or(query_variation)
    '''

    def __init__(self, query_str, as_phrase=True, escape=False, sanitize=False):
        '''
        Initialize a query with given parameters
        '''
        self.query_str = query_str

        if escape:
            self._escape_special_chars()

        if sanitize:
            self._sanitize()

        if as_phrase:
            self._as_phrase()

    def __str__(self):
        '''
        Return query as a string
        '''
        return self.query_str

    def boost_importance(self, factor):
        '''
        Return new query that raises the immportance of this
        query to given factor
        '''
        return Query(
            '({})^{}'.format(self.query_str, str(factor)),
            as_phrase=False
        )

    def select_and(self, query):
        '''
        Return new query that joins this query and another query
        with an AND select
        '''
        return Query(
            '{} AND {}'.format(self.query_str, str(query)),
            as_phrase=False
        )

    def select_or(self, query):
        '''
        Return new query that joins this query and another query
        with an OR select
        '''
        return Query(
            '{} OR {}'.format(self.query_str, str(query)),
            as_phrase=False
        )

    def select_require(self, terms):
        '''
        Make query require the given terms
        '''
        if len(terms) == 0:
            return self

        new_query_str = self.query_str
        for term in terms:
            new_query_str += '+{}'.format(term)
        return Query(
            new_query_str,
            as_phrase=False
        )

    def for_single_field(self, field):
        '''
        Apply given field to query
        '''
        if field == "":
            return self

        return Query(
            '{}:{}'.format(field, self.query_str),
            as_phrase=False
        )

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

        return Query(
            '{}~{}'.format(self.query_str, factor),
            as_phrase=False
        )

    def for_fields(self, fields):
        '''
        Apply given fields to query
        '''
        if type(fields) is not dict:
            raise ValueError('Fields must be a dict of field names and boost factors')

        return Query(
            self.query_str,
            as_phrase=False
        ).select_or(self._for_fields_helper(self.query_str, list(fields.items())))

    def _for_fields_helper(self, query_str, fields):
        field, boost = fields[0]
        query = Query(query_str, as_phrase=False).boost_importance(boost)
        query = Query(
            '{}:{}'.format(field, str(query)),
            as_phrase=False
        )
        if fields[1:]:
            return query.select_or(query._for_fields_helper(query_str, fields[1:]))
        else:
            return query

    ##################
    # INIT MODIFIERS #
    ##################

    def _as_phrase(self):
        '''
        Format query as entire phrase, and optionally set proximity for
        words within the phrase.
        '''
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
        new_query_str = ' '.join(words_list)
        self.query_str = new_query_str if len(new_query_str)>0 else self.query_str

    def _escape_special_chars(self):
        '''
        Escape special characters that interfere with Solr's query parser.
        Ideally only use on queries where as_phrase=False, since special
        characters in phrases do not upset Solr.
        '''
        special_chars = ['!', '(', ')', '{', '}', '[', ']', '^', '"', '~', '*', '?', ':', '|', '&']
        for c in special_chars:
            self.query_str = self.query_str.replace(c, '\\'+c)
