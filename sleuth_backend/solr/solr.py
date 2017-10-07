import pysolr
from sleuth_backend.settings import HAYSTACK_CONNECTIONS

solr_url = HAYSTACK_CONNECTIONS['default']['URL']
solr_core = "test"
solr_db = pysolr.Solr(solr_url + solr_core, timeout=10)

def add_item(item):
    """
    Add item to Solr
    """
    solr_db.add([item])
