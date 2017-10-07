import pysolr

solrDb = pysolr.Solr('http://localhost:8983/solr/', timeout=10)

def add_item(item):
    """
    Add 
    """
    solrDb.add([item])
