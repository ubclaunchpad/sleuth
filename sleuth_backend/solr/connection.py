import pysolr
import json

class SolrConnection(object):
    """
    Connection to Solr database
    """
    
    def __init__(self, url):
        """
        Creates a SolrConnection form the given base Solr url of the form
        'http://solrhostname:solrport/solr'.
        """
        self.url = url
        self.solr = pysolr.Solr(url, timeout=10)
        self.solr_admin = pysolr.SolrCoreAdmin(url + '/admin/cores')  
        self.cores = {}

        for core_name in self.fetch_core_names():
            self.cores[core_name] = pysolr.Solr(self.url + '/' + core_name)

    def fetch_core_names(self):
        """
        Makes a request to Solr and returns an array of strings where each 
        string is the name of a core in the response from Solr.
        """
        status_response = self.solr_admin.status()
        status = json.loads(status_response)
        return [core_name for core_name in status['status']]

    def core_names(self):
        """
        Returns a list of know cores in the Solr instance without making a 
        request to Solr.
        """
        return list(self.cores.keys())

    def fetch_core_schema(self, name):
        """
        Returns the schema of the core with the given name as a dictionary.
        """
        response = self.solr_admin._get_url(self.url + '/' + name + '/schema')
        body = json.loads(response)

        if 'schema' not in body:
            raise ValueError('Solr did not return a schema. Are you sure the core' + 
                ' name {} is an existing core?'.format(name))
        
        return body['schema']

    def insert_document(self, core, doc):
        """
        Attempts to insert the given document (a dict) into the solr core with
        the given name and returns the response from Solr. All values in 'doc' 
        must be strings.
        """
        if core not in self.cores:
            raise ValueError("A core for the document type {} was not found".format(core))
        return self.cores[core].add([doc])

    def search(self, core_name, search_term):
        """
        Performs a search of the core with the given name on the Solr instance and 
        returns an array of document info for documents that matched the search term.
        Raises a pysolr.SolrError if the search request to Solr fails, or a 
        KeyError if a core with the given name does not exist.
        """
        try:
            core = self.cores[core_name]
        except KeyError as e:
            raise KeyError('No Solr core with the name "{}" was found'.format(core_name))
        
        return [self.__create_simple_document(result) for result in core.search(search_term)]

    def optimize(self, core_name=None):
        """
        Performs defragmentation of all/specified core(s) in Solr database
        Optionally accepts ``core_name``. Default is ``None`
        """
        if core_name:
            try:
                self.cores[core_name].optimize()
            except KeyError as e:
                raise KeyError('No Solr core with the name "{}" was found'.format(core_name))
        else:
            for core in self.core_names():
                self.cores[core].optimize()

    def __create_simple_document(self, document_details):
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
