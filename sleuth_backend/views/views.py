import pysolr
import re
import json
from django.http import HttpResponse
from .error import SleuthError, ErrorTypes
from sleuth_backend.solr import connection as solr
from sleuth.settings import HAYSTACK_CONNECTIONS
from sleuth_backend.solr.query import Query

SOLR = solr.SolrConnection(HAYSTACK_CONNECTIONS['default']['URL'])
DEFAULT_CORE = "test"

def cores(request):
    '''
    Returns a JSON array of the name of each core in our Solr system.

    Example Response Body:
    ['core1', 'core2']
    '''
    if request.method != 'GET':
        return HttpResponse(status=405)

    return HttpResponse(json.dumps(SOLR.core_names()), status=200)

def search(request):
    '''
    Takes a GET request containing a search term and returns results from the
    connected Solr instance.

    Params:
        core: (optional) the name of the core to search in. search all cores by default
        q: the term or phrase to search for
        sort: see Solr docs for sort syntax
        start: the index of the first result to return
        rows: the number of results to return starting from the start index
        return: the desired return fields. see sleuth_backend.solr.models

    Example Usage:
    http:// ... /api/search/?q=hello&core=genericPage&return=children

    Example Response Body: 
    {
        "data": [
            {
                "type": <core name>,
                "response": {
                    "numFound": <number of results found for query>,
                    "start": <index of first result (paging option)>,
                    "docs": [
                        {
                            <document format depends on core>
                        }, {
                            <see sleuth_backend.solr.models for core schemas>
                        }
                    ]
                },
                "highlighting": {
                    "<id of first document>": {
                        "content": ['this is the highlight of the first result']
                    },
                    "<id of second document>": {
                        "content" ['this is the highlight of the second result']
                    }
                }
            },
            {
                "type": <other core name>,
                "response": { ... },
                "highlighting": { ... }
            }
        ]
    }

    '''
    if request.method != 'GET':
        return HttpResponse(status=405)

    core = request.GET.get('core', '')
    query = request.GET.get('q', '')
    requested_return_fields = request.GET.get('return', '')
    return_fields = 'id,updatedAt,name,description'
    if requested_return_fields is not '':
        return_fields = ',' + requested_return_fields

    kwargs = {
        'sort': request.GET.get('sort', ''),
        'start': request.GET.get('start', ''),
        'rows': request.GET.get('rows', ''),
        'return_fields': return_fields,
    }

    if query is '':
        sleuth_error = SleuthError(ErrorTypes.INVALID_SEARCH_REQUEST)
        return HttpResponse(sleuth_error.json(), status=400)

    cores_to_search = []
    if core is '':
        for c in SOLR.core_names():
            cores_to_search.append(c)
    else:
        cores_to_search.append(core)

    responses = {
        'data':[]
    }
    for core_to_search in cores_to_search:
        try:
            query, kwargs = _build_search_query(core_to_search, query, kwargs)
            query_response = SOLR.query(core_to_search, query, **kwargs)
            query_response['type'] = core_to_search
            responses['data'].append(query_response)

        # Handle errors and exceptions from each query
        except pysolr.SolrError as s_e:
            sleuth_error = SleuthError(ErrorTypes.SOLR_SEARCH_ERROR, str(s_e))
            return HttpResponse(sleuth_error.json(), status=400)
        except KeyError as k_e:
            sleuth_error = SleuthError(ErrorTypes.UNEXPECTED_SERVER_ERROR, str(k_e))
            return HttpResponse(sleuth_error.json(), status=500)
        except ValueError as v_e:
            sleuth_error = SleuthError(ErrorTypes.SOLR_CONNECTION_ERROR, str(v_e))
            return HttpResponse(sleuth_error.json(), status=500)
        if 'error' in query_response:
            sleuth_error = SleuthError(
                ErrorTypes.SOLR_SEARCH_ERROR,
                message=query_response['error']['msg']
            )
            return HttpResponse(sleuth_error.json(), status=query_response['error']['code'])

    return HttpResponse(pysolr.force_unicode(responses))

def _build_search_query(core, query_str, kwargs):
    '''
    Builds a serach query and sets parameters that is most likely to
    return the best results for the given core using the given user query.
    
    See https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html
    for more information about Apache Lucene query syntax.
    '''

    if core == 'genericPage':
        fields = {
            'id': 1,
            'siteName': 10,
            'name': 10,
            'description': 5,
            'content': 2
        }
        query = Query(query_str, fields=fields, proximity=5)
        terms_query = Query(query_str, fields=fields, as_phrase=False)
        query.select_or(terms_query)
        kwargs['default_field'] = 'description'
        kwargs['highlight_fields'] = 'content'

    elif core == 'courseItem':
        fields = {
            'id': 1,
            'name': 10,
            'description': 10,
            'subjectData': 5,
        }
        query = Query(query_str, fields=fields, proximity=5)
        terms_query = Query(query_str, fields=fields, as_phrase=False)
        query.select_or(terms_query)
        kwargs['default_field'] = 'description'
        kwargs['highlight_fields'] = 'description'

    else:
        query = Query(query_str)

    return (str(query), kwargs)
