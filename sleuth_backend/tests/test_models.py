from django.test import TestCase
from sleuth_backend.solr.models import SolrDocument, GenericPage
from unittest.mock import MagicMock

class TestGenericPage(TestCase):
    
    def create_page(self):
        args = {
            "id": "testid",
            "type": "genericPage",
            "siteName": "testname",
            "updatedAt": "9827359348752937402",
            "pageName": "testpage",
            "pageTitle": "testtitle",
            "content": "testcontent",
            "description": "testblurb",
            "children": []
        }
        return (args, GenericPage(**args))
    
    def test_init(self):
        args, page = self.create_page()
        
        for (key, value) in args.items():
            self.assertEqual(value, page.doc[key])

    def test_output_format(self):
        args, page = self.create_page()
        self.assertEqual(
            {
                "id": args["id"],
                "type": args["type"],
                "siteName": args["siteName"],
                "data": {
                    "updatedAt": args["updatedAt"],
                    "pageName": args["pageName"],
                    "pageTitle": args["pageTitle"],
                    "description": args["description"]
                }
            },
            page.output_format()
        )

    def test_type(self):
        _, page = self.create_page()
        self.assertEqual(page.type(), "genericPage")

    def test_save_to_solr(self):
        args, page = self.create_page()
        mock = MagicMock()
        mock.insert_document.return_value = None
        page.save_to_solr(mock)
        mock.insert_document.assert_called_with("genericPage", args)
