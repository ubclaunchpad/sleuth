import pysolr

solr_url = 'http://localhost:8983/solr/'
solr_db = pysolr.Solr(solr_url, timeout=10)

def add_item(item):
    """
    Add item to Solr
    """
    solr_db.add([item])
