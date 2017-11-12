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
                return req.replace(callback=course_parser.parse_subjects)
            else:
                return
        
        return req
        
    def parse_generic_item(self, response):
        """
        Points to generic_page_parser (the default parser for this crawler)
        """
        links = []
        for link in self.GENERIC_LINK_EXTRACTOR.extract_links(response):
            if link.url != response.url:
                links.append(link.url)
        return generic_page_parser.parse_generic_item(response, links)
