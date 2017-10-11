import pysolr
import json
from sleuth.settings import HAYSTACK_CONNECTIONS

# Begin config

SOLR_URL = HAYSTACK_CONNECTIONS['default']['URL']
SOLR_ADMIN = pysolr.SolrCoreAdmin(SOLR_URL + '/admin/cores')
SOLR_DB = pysolr.Solr(SOLR_URL, timeout=10)

def cores():
    """
    Returns a list of strings, where each string is the name of a Solr core.
    """
    status_response = SOLR_ADMIN.status()
    status = json.loads(status_response)
    return [core_name for core_name in status['status']]

def __create_pysolr_cores(core_names):
    """
    Returns a mapping from core name to pysolr core object.
    """
    solr_cores = {}
    for core_name in core_names:
        solr_cores[core_name] = pysolr.Solr(SOLR_URL + '/' + core_name)
    return solr_cores

SOLR_CORES = __create_pysolr_cores(cores())
DEFAULT_CORE = "test"

# End config

def add_item(item, resource_type=DEFAULT_CORE):
    """
    Add item to Solr core based on the resource type.
    """
    SOLR_CORES[resource_type].add([item])

def search(search_term, core_name=DEFAULT_CORE):
    """
    Performs a search of the core with the given name on the Solr instance and 
    returns an array of document info for documents that matched the search term.
    Raises a pysolr.SolrError if the search request to Solr fails, or a 
    KeyError if a core with the given name does not exist.
    """
    try:
        core = SOLR_CORES[core_name]
    except KeyError as e:
        raise KeyError('No Solr core with the name "{}" was found'.format(core_name))
    
    return [__create_simple_document(result) for result in core.search(search_term)]

def __create_simple_document(document_details):
    """TODO: improve
    Returns a dictionary of the following format using the given document
    details:
    {
        "id": "/opt/solr/example/exampledocs/solr-word.pdf",
        "date": "2008-11-13T13:35:51Z"
        "keywords": "solr, word, pdf"
        "format": "application/pdf",
        "title": "solr-word",
        "creator": "Grant Ingersoll"
    }
    """
    attributes = ['id', 'date', 'keywords', 'format', 'title', 'creator']
    doc = {}

    for attr in attributes:
        # We have to do this check because keys are strings and values are arrays
        # in the Solr JSON responses.
        if attr in document_details.keys() and len(document_details[attr]) > 0:
            doc[attr] = document_details[attr][0]
    return doc
