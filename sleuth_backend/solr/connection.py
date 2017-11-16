import pysolr
import json
import requests

class SolrConnection(object):
    """
    Connection to Solr database
    """

    def __init__(self, url):
        """
        Creates a SolrConnection form the given base Solr url of the form
        'http://<solrhostname>:<port>/solr'.
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
        Returns a list of known valid cores in the Solr instance without
        making a request to Solr - this request excludes cores used for testing.
        """
        valid_cores = list(self.cores.keys())
        if 'test' in valid_cores:
            valid_cores.remove('test')
        return valid_cores

    def fetch_core_schema(self, name):
        """
        Returns the schema of the core with the given name as a dictionary.
        """
        response = self._get_url("{}/{}/schema".format(self.url, name), {})

        if 'schema' not in response:
            raise ValueError('Solr did not return a schema. Are you sure ' + \
                'the core named "{}" is an existing core?'.format(name))

        return response['schema']

    def insert_document(self, core, doc):
        """
        Attempts to insert the given document (a dict) into the solr core with
        the given name and returns the response from Solr. All values in 'doc'
        must be strings.
        """
        if core not in self.cores:
            raise ValueError("A core for the document type {} was not found".format(core))
        return self.cores[core].add([doc])

    def query(self, core, query, sort="", start="", rows="", default_field="",
        search_fields="", return_fields="", highlight_fields="", omit_header=True):
        """
        Returns the response body from Solr corresponding to the given query.
        See https://lucene.apache.org/solr/guide/6_6/common-query-parameters.html
        and https://lucene.apache.org/solr/guide/6_6/highlighting.html
        for common query parameters and parameter formatting.

        Params (See Solr docs link above for details):
            core (str): The name of the Solr core to search in.
            query (str): The string to search the core for.
            sort (str): The field to sort results on, and the sort order (see
                        Solr docs for details).
            start (int): Specifies an offset into a query’s result set and instructs
                        Solr to begin displaying results from this offset.
            rows (int): The maximum number of documents from the complete result
                        set that Solr should return.
            default_field (str): The default field to search in.
            search_fields (str): Defines a query that can be used to restrict
                        the superset of documents that can be returned, without
                        influencing score.
            return_fields (str): Limits the information included in a query
                        response to a specified list of fields.
            highlight_fields (str): Specifies a list of fields to highlight.
            omit_header (bool): Whether or not Solr should include a header with
                        metadata about the query in its response.
        """
        params = {
            "q": query,
            "wt": "json",
            "df": default_field,
            "omitHeader": "true" if omit_header else "false",
            "hl.fragsize": 200
        }
        if sort is not "":
            params["sort"] = sort
        if start is not "":
            params["start"] = start
        if rows is not "":
            params["rows"] = rows
        if search_fields is not "":
            params["fq"] = search_fields
        if return_fields is not "":
            params["fl"] = return_fields
        if highlight_fields is not "":
            params["hl"] = "on"
            params["hl.fl"] = highlight_fields

        return self._get_url("{}/{}/select".format(self.url, core), params)

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
            for core in self.cores:
                self.cores[core].optimize()

    def _get_url(self, url, params):
        """
        Makes a request to the given url relative to the base url with the given
        parameters and returns the response as a JSON string.
        """
        response = requests.get(url, params=pysolr.safe_urlencode(params))
        return response.json()
