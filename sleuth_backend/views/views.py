import pysolr
import re
import json
from django.http import HttpResponse
from . import error
from sleuth_backend.solr import solr

def cores(request):
    '''
    Returns a JSON array of the name of each core in our Solr system.
    '''
    if request.method != 'GET':
        return HttpResponse(status=405)

    return HttpResponse(json.dumps(solr.cores()), status=200)

def search(request):
    '''
    Takes a GET request containing a search term and returns results from the
    connected Solr instance. The request should contain the 'q' parameter with
    a search term (i.e q=my_search_term), or a search phrase in double quotes
    (i.e q="my search phrase").
    '''
    if request.method != 'GET':
        return HttpResponse(status=405)

    search_term = request.GET.get('q', '')
    if search_term is '':
        sleuth_error = error.SleuthError(
            'Must supply a search term with the parameter "q".',
            error.ErrorTypes.INVALID_SEARCH_TERM
        )
        return HttpResponse(sleuth_error.json(), status=400)

    try:
        json_data = json.dumps(solr.search(search_term))
    except pysolr.SolrError as e:
        sleuth_error = error.SleuthError(str(e), error.ErrorTypes.SOLR_SEARCH_ERROR)
        return HttpResponse(sleuth_error.json(), status=400)
    except KeyError as e:
        sleuth_error = error.SleuthError(
            "An error occurred processing the request",
            error.ErrorTypes.UNEXPECTED_SERVER_ERROR
        )
        return HttpResponse(sleuth_error.json(), status=500)
    except ValueError as e:
        sleuth_error = error.SleuthError(
            str(e), 
            error.ErrorTypes.SOLR_CONNECTION_ERROR
        )
        return HttpResponse(sleuth_error.json(), status=500)

    return HttpResponse(json_data)