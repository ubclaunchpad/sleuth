'''
Sleuth's Django API
'''

import pysolr
import re
import json
import sys
from django.http import HttpResponse
from .error import SleuthError, ErrorTypes
from .views_utils import *
from sleuth_backend.solr import connection as solr
from sleuth.settings import HAYSTACK_CONNECTIONS

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
        type: (optional) the name of the core to search in - all cores by default
        q: the term or phrase to search for
        sort: see Solr docs for sort syntax
        start: the index of the first result to return
        rows: the number of results to return starting from the start index
        return: the desired return fields - see sleuth_backend.solr.models
        state: any string to be returned in response

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
        ],
        "request": { <data about your original request, state will be here too> }
    }

    '''
    if request.method != 'GET':
        return HttpResponse(status=405)

    cores_to_search = build_core_request(request.GET.get('type', ''), SOLR.core_names())
    query = request.GET.get('q', '')
    state = request.GET.get('state', '')
    return_fields = build_return_fields(request.GET.get('return', ''))

    kwargs = {
        'sort': request.GET.get('sort', ''),
        'start': request.GET.get('start', ''),
        'rows': request.GET.get('rows', ''),
        'return_fields': return_fields,
    }

    if query is '':
        sleuth_error = SleuthError(ErrorTypes.INVALID_SEARCH_REQUEST)
        return HttpResponse(sleuth_error.json(), status=400)

    responses = {
        'data':[]
    }
    for core_to_search in cores_to_search:
        try:
            new_query, new_kwargs = build_search_query(core_to_search, query, kwargs)
            query_response = SOLR.query(core_to_search, new_query, **new_kwargs)
            if 'error' in query_response:
                sleuth_error = SleuthError(
                    ErrorTypes.SOLR_SEARCH_ERROR,
                    message=query_response['error']['msg']+" on core "+core_to_search
                )
                return HttpResponse(sleuth_error.json(), status=query_response['error']['code'])
            
            # Attach type to response and flatten single-item list fields
            query_response['type'] = core_to_search
            for doc in query_response['response']['docs']:
                flatten_doc(doc, return_fields)

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

    responses['request'] = {
        'query': query,
        'types': cores_to_search,
        'return_fields': return_fields.split(","),
        'state': state
    }
    return HttpResponse(pysolr.force_unicode(responses))
