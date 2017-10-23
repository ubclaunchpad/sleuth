import json
import time
from . import connection as solr

class SolrDocument(object):
    """
    An base class for documents that are inserted into Solr, an retured as 
    search results from the Sleuth API.
    """

    def __init__(self, doc, **kwargs):
        """
        This method should be called by the subclass constructor.
        """
        self.doc = doc
        for key in self.doc.keys():
            if key in kwargs and key is not "type":
                doc[key] = kwargs[key]

    def output_format(self):
        """
        Returns the document in JSON format as it is supposed to be returned 
        from a Sleuth API response. This method must be overridden.
        """
        pass

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
        "siteName": "",
        "updatedAt": "",
        "pageName": "",
        "description": "",
        "content": "",
        "children": []
    }

    def __init__(self, **kwargs):
        super(GenericPage, self).__init__(self.doc, **kwargs)

    def output_format(self):
        return {
            "id": self.doc['id'],
            "type": self.doc['type'],
            "siteName": self.doc['siteName'],
            "data": {
                "updatedAt": self.doc['updatedAt'],
                "pageName": self.doc['pageName'],
                "description": self.doc['description']
            }
        }

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

    def output_format(self):
        return {
            "id": self.doc['id'],
            "type": self.doc['type'],
            "name": self.doc['name'],
            "data": {
                "updatedAt": self.doc['updatedAt'],
                "description": self.doc['description'],
                "subject": {
                    "subjectId": self.doc['subjectId'],
                    "subjectData": []
                }
            }
        }
