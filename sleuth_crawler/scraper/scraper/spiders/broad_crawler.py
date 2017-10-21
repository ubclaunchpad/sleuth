import scrapy
from sleuth_crawler.scraper.scraper.spiders.parsers import generic_page_parser, course_parser
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from sleuth_crawler.scraper.scraper.settings import PARENT_URLS

class BroadCrawler(CrawlSpider):
    """
    Spider that broad crawls starting at list of predefined URLs
    """
    name = "broad_crawler"

    GENERIC_LINK_EXTRACTOR = LinkExtractor(
        allow=(r'ubc', r'universityofbc', ),
        deny=(r'accounts\.google', r'intent', )
    )

    start_urls = PARENT_URLS
    rules = (
        Rule(
            GENERIC_LINK_EXTRACTOR,
            follow=True,
            process_request='process_req',
            callback='parse_generic_item'
        ),
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.SolrPipeline': 400,
        }
    }

    def process_req(self, req):
        """
        Work on requests to identify those that qualify for special treatment
        """
        # Parse courses
        course_root = "courses.students.ubc.ca"
        if course_root in req.url:
            if "cs/main?pname=subjarea&tname=subjareas&req=0" in req.url:
                return req.replace(callback=self.parse_subjects)
            else:
                return
        
        return req
        
    """
    Functions pointing to parser modules
    """
    def parse_generic_item(self, response):
        return generic_page_parser.parse_generic_item(response, self.GENERIC_LINK_EXTRACTOR)

    def parse_subjects(self, response):
        return course_parser.parse_subjects(response)

    def parse_subjects_helper(self, response):
        return course_parser.parse_course_helper(response)

    def parse_course_details(self, response):
        return course_parser.parse_course_details(response)
