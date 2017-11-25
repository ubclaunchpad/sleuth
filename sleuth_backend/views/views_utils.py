'''
Helper methods for Django views
'''

from pysolr import SolrError
from .error import SleuthError, ErrorTypes
from sleuth_backend.solr.query import Query

def build_core_request(core, solr_cores):
    '''
    Builds a list of cores to search based on given core parameter
    '''
    return [c for c in solr_cores] if core is '' else [core]

def build_return_fields(fields):
    '''
    Builds a string listing the fields to return
    '''
    return_fields = 'id,updatedAt,name,description'
    if fields is not '':
        return_fields = return_fields + ',' + fields
    return return_fields

def flatten_doc(doc, return_fields):
    '''
    Flattens single-item list fields returned by Solr
    '''
    for f in return_fields.split(","):
        if f in doc:
            doc[f] = doc[f][0] if len(doc[f]) == 1 else doc[f]
        else:
            doc[f] = ''
    return doc

def build_search_query(core, query_str, base_kwargs):
    '''
    Builds a search query and sets parameters that is most likely to
    return the best results for the given core using the given user query.
    
    See https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html
    for more information about Apache Lucene query syntax.
    '''
    kwargs = base_kwargs.copy()

    if core == 'genericPage':
        fields = {
            'id': 1,
            'name': 8,
            'siteName': 5,
            'description': 5,
            'content': 8
        }
        query = Query(query_str) \
            .fuzz(2) \
            .boost_importance(5)
        terms_query = Query(query_str, as_phrase=False, escape=True, sanitize=True) \
            .fuzz(1) \
            .for_fields(fields)
        query = query.select_or(terms_query)
        kwargs['default_field'] = 'content'
        kwargs['highlight_fields'] = 'content,description'

    elif core == 'courseItem':
        fields = {
            'id': 1,
            'name': 9,
            'description': 8,
            'subjectData': 5,
        }
        query = Query(query_str).fuzz(2)
        terms_query = Query(query_str, as_phrase=False, escape=True, sanitize=True) \
            .for_fields(fields)
        query = query.select_or(terms_query)
        kwargs['default_field'] = 'name'
        kwargs['highlight_fields'] = 'description'

    elif core == 'redditPost':
        fields = {
            'id': 1,
            'name': 7,
            'description': 10,
            'comments': 6,
        }
        query = Query(query_str).fuzz(1)
        terms_query = Query(query_str, as_phrase=False, escape=True, sanitize=True) \
            .for_fields(fields)
        query = query.select_or(terms_query)
        kwargs['default_field'] = 'name'
        kwargs['highlight_fields'] = 'description,comments'

    else:
        query = Query(query_str)

    return (str(query), kwargs)

def build_getdocument_query(doc_id, base_kwargs):
    '''
    Builds a query and sets parameters to find the document associated with
    the given doc_id, allowing for a missing/extra trailing "/" on the doc_id
    '''
    kwargs = base_kwargs.copy()
    query = Query(doc_id, as_phrase=False, escape=True).for_single_field('id') \
        .select_or(
            Query(doc_id + '/', as_phrase=False, escape=True).for_single_field('id')
        ) \
        .select_or(
            Query(doc_id.rstrip('/'), as_phrase=False, escape=True).for_single_field('id')
        )
    kwargs['default_field'] = 'id'
    return (str(query), kwargs)

def build_error(err):
    '''
    Builds appropriate error and response status for given Exception.
    Used specifically in views for catching exceptions that could be thrown
    by a Solr query
    '''
    if isinstance(err, SolrError):
        sleuth_error = SleuthError(ErrorTypes.SOLR_SEARCH_ERROR, str(err))
        return sleuth_error.json(), 400
    elif isinstance(err, KeyError):
        sleuth_error = SleuthError(ErrorTypes.UNEXPECTED_SERVER_ERROR, str(err))
        return sleuth_error.json(), 500
    elif isinstance(err, ValueError):
        sleuth_error = SleuthError(ErrorTypes.SOLR_CONNECTION_ERROR, str(err))
        return sleuth_error.json(), 500
