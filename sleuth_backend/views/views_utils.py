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
    cores_to_search = []
    if core is '':
        for c in solr_cores:
            cores_to_search.append(c)
    else:
        cores_to_search.append(core)
    return cores_to_search

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
    kwargs = base_kwargs

    if core == "genericPage":
        fields = {
            'id': 1,
            'siteName': 8,
            'name': 8,
            'description': 5,
            'content': 2
        }
        query = Query(query_str)
        query.fuzz(2)
        terms_query = Query(query_str, as_phrase=False, escape=True)
        terms_query.fuzz(2)
        terms_query.for_fields(fields)
        query.select_or(terms_query)
        kwargs['default_field'] = 'content'
        kwargs['highlight_fields'] = 'content'

    elif core == "courseItem":
        fields = {
            'id': 1,
            'name': 9,
            'description': 8,
            'subjectData': 5,
        }
        query = Query(query_str)
        query.fuzz(2)
        terms_query = Query(query_str, as_phrase=False, escape=True)
        terms_query.for_fields(fields)
        query.select_or(terms_query)
        kwargs['default_field'] = 'name'
        kwargs['highlight_fields'] = 'description'

    else:
        query = Query(query_str)

    return (str(query), kwargs)

def build_getdocument_query(doc_id, base_kwargs):
    '''
    Builds a query and sets parameters to find the document associated with
    the given doc_id
    '''
    kwargs = base_kwargs
    query = Query(doc_id, as_phrase=False, escape=True)
    query.for_single_field('id')
    kwargs['default_field'] = 'id'
    return (str(query), kwargs)

def build_error(err):
    '''
    Builds appropriate error and response status for given Exception
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
