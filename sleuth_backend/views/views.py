import pysolr
import re
import json
from django.http import HttpResponse
from .error import SleuthError, ErrorTypes
from sleuth_backend.solr import connection as solr
from sleuth.settings import HAYSTACK_CONNECTIONS
from sleuth_backend.solr.query_builder import Query, QueryBuilder

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
        core: the name of the core to search in
        q: the term or phrase to search for
        sort: see Solr docs for sort syntax
        start: the index of the first result to return
        rows: the number of results to return starting from the start index

    Example Response Body:
    {
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
                "content": ['this is the hilighted portion of the first result']
            },
            "<id of second document>": {
                "content" ['this is the hilighted portion of the second result']
            }
        }
    }
    '''
    if request.method != 'GET':
        return HttpResponse(status=405)

    core = request.GET.get('core', '')
    query = request.GET.get('q', '')
    kwargs = {
        'sort': request.GET.get('sort', ''),
        'start': request.GET.get('start', ''),
        'rows': request.GET.get('rows', ''),
        'default_field': 'content',
        'return_fields': 'id,siteName,updatedAt,pageName,description',
        'highlight_fields': 'content',
    }

    if core is '' or query is '':
        sleuth_error = SleuthError(ErrorTypes.INVALID_SEARCH_REQUEST)
        return HttpResponse(sleuth_error.json(), status=400)

    query = __build_search_query(query, core)

    try:
        query_response = SOLR.query(core, query, **kwargs)
        response = json.loads(query_response)
    except pysolr.SolrError as e:
        sleuth_error = SleuthError(ErrorTypes.SOLR_SEARCH_ERROR, str(e))
        return HttpResponse(sleuth_error.json(), status=400)
    except KeyError:
        sleuth_error = SleuthError(ErrorTypes.UNEXPECTED_SERVER_ERROR)
        return HttpResponse(sleuth_error.json(), status=500)
    except ValueError:
        sleuth_error = SleuthError(ErrorTypes.SOLR_CONNECTION_ERROR)
        return HttpResponse(sleuth_error.json(), status=500)

    if 'error' in response:
        sleuth_error = SleuthError(
            ErrorTypes.SOLR_SEARCH_ERROR,
            message=response['error']['msg']
        )
        return HttpResponse(sleuth_error.json(), status=response['error']['code'])
    return HttpResponse(query_response)

def __build_search_query(query_str, core):
    '''
    Builds a serach query that is most likely to return the best results
    for the given core using the given user query. See
    https://lucene.apache.org/solr/guide/6_6/the-standard-query-parser.html
    for more information about Apache Lucene query syntax.
    '''
    query = Query(query_str)
    builder = QueryBuilder()

    # Set detailed query format and args to match the core you are querying
    if core == 'genericPage':
        fields = {
            'id': 1,
            'siteName': 10,
            'pageName': 10,
            'description': 5,
            'content': 2
        }
        phrase_query = builder.build_query(query_str, fields, as_phrase=True)
        terms_query = builder.build_query(query_str, fields)
        query = phrase_query.or_op(terms_query)

    # TODO: add a case to support course search

    return str(query)