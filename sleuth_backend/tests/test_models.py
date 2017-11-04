from django.test import TestCase
from sleuth_backend.solr.models import SolrDocument, GenericPage, CourseItem
from unittest.mock import MagicMock

class TestModels(TestCase):
    """
    Test Solr document types
    """
    def create_page(self, t):
        if t == "genericPage":
            args = {
                "id": "testid",
                "type": "genericPage",
                "name": "testname",
                "updatedAt": "9827359348752937402",
                "siteName": "testsite",
                "content": "testcontent",
                "description": "testblurb",
                "children": []
            }
            return (args, GenericPage(**args))
        if t == "courseItem":
            args = {
                "id": "test101",
                "type": "courseItem",
                "name": "testname",
                "updatedAt": "1234",
                "description": "testdescription",
                "subjectId": "test",
                "subjectData": []
            }
            return (args, CourseItem(**args))

    def test_init(self):
        args, page = self.create_page("genericPage")
        for (key, value) in args.items():
            self.assertEqual(value, page.doc[key])

    def test_output_formats(self):
        args, page = self.create_page("genericPage")
        self.assertEqual(
            {
                "id": args["id"],
                "type": args["type"],
                "name": args["name"],
                "data": {
                    "updatedAt": args["updatedAt"],
                    "siteName": args["siteName"],
                    "description": args["description"]
                }
            },
            page.output_format()
        )
        args, page = self.create_page("courseItem")
        self.assertEqual(
            {
                "id": args['id'],
                "type": args['type'],
                "name": args['name'],
                "data": {
                    "updatedAt": args['updatedAt'],
                    "description": args['description'],
                    "subject": {
                        "subjectId": args['subjectId'],
                        "subjectData": args['subjectData']
                    }
                }
            },
            page.output_format()
        )

    def test_type(self):
        _, page = self.create_page("genericPage")
        self.assertEqual(page.type(), "genericPage")

    def test_save_to_solr(self):
        args, page = self.create_page("genericPage")
        mock = MagicMock()
        mock.insert_document.return_value = None
        page.save_to_solr(mock)
        mock.insert_document.assert_called_with("genericPage", args)
