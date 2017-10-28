class Query(object):

    def __init__(self, query_str, field=None):
        self.query_str = query_str

    def __str__(self):
        return self.query_str

    def as_phrase(self):
        return Query('"{}"'.format(self.query_str))

    def boost(self, factor):
        return Query('({})^{}'.format(self.query_str, str(factor)))

    def and_op(self, query):
        return Query('{} AND {}'.format(self.query_str, str(query)))

    def or_op(self, query):
        return Query('{} OR {}'.format(self.query_str, str(query)))

    def require(self, terms):
        new_query_str = self.query_str

        for term in terms:
            new_query_str += '+{}'.format(term)

        return Query(new_query_str)

    def for_fields(self, fields):
        return self._for_fields_helper(self.query_str, list(fields.items()))

    def _for_fields_helper(self, query_str, fields):
        if not fields:
            return Query(query_str)

        field, boost = fields[0]
        query = Query(query_str).boost(boost)
        query = Query('{}:{}'.format(field, str(query)))
        return query.or_op(query._for_fields_helper(query_str, fields[1:]))

class QueryBuilder(object):

    def __init__(self):
        pass

    def build_query(self, string, fields, as_phrase=False):
        if len(fields) == 0:
            raise ValueError('Must supply at least one field to search in')
        if type(fields) is not dict:
            raise ValueError('Fields must be a dict of field names and boost factors')

        string = self._sanitize(string)
        # TODO: trim useless words like 'and', 'or', 'for' from query if as_phrase
        # is false using NLTK POS tagger if it's not a phrase

        query = Query(string)

        if as_phrase:
            query = query.as_phrase()

        return query.for_fields(fields)

    def _sanitize(self, string):
        return ' '.join(string.split())
