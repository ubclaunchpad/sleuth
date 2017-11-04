import json
import time
from . import connection as solr

class SolrDocument(object):
    """
    An base class for documents that are inserted into Solr, an retured as 
    search results from the Sleuth API.
    """

    # Default doc fields: all subtypes must at least have these fields
    doc = {
        "id": "",
        "type": "",
        "name": "",
        "updatedAt": "",
        "description": ""
    }

    def __init__(self, doc, **kwargs):
        """
        This method should be called by the subclass constructor.
        """
        self.doc = doc
        for key in self.doc.keys():
            if key in kwargs and key is not "type":
                doc[key] = kwargs[key]

    def save_to_solr(self, solr_connection):
        """
        Submits the document to the given Solr connection. This method should not
        be overridden.
        """
        solr_connection.insert_document(self.type(), self.doc)

    def type(self):
        """
        Returns a string representing the document type. This method should not
        be overridden.
        """
        return self.doc["type"]

class GenericPage(SolrDocument):
    """
    Represents a generic web page.
    """
    doc = {
        "id": "",
        "type": "genericPage",
        "name": "",
        "updatedAt": "",
        "siteName": "",
        "description": "",
        "content": "",
        "children": []
    }

    def __init__(self, **kwargs):
        super(GenericPage, self).__init__(self.doc, **kwargs)

class CourseItem(SolrDocument):
    """
    Represents a UBC course.
    """
    doc = {
        "id": "",
        "type": "courseItem",
        "name": "",
        "updatedAt": "",
        "description": "",
        "subjectId": "",
        "subjectData": []
    }

    def __init__(self, **kwargs):
        super(CourseItem, self).__init__(self.doc, **kwargs)
