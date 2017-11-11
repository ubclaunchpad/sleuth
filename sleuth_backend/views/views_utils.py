'''
Helper methods for Django views
'''

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
            'siteName': 10,
            'name': 10,
            'description': 5,
            'content': 2
        }
        query = Query(query_str, fields=fields, proximity=5)
        terms_query = Query(query_str, fields=fields, as_phrase=False)
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
        query = Query(query_str, fields=fields)
        kwargs['default_field'] = 'name'
        kwargs['highlight_fields'] = 'description'

    else:
        query = Query(query_str)

    return (str(query), kwargs)
