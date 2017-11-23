import scrapy
from sleuth_crawler.scraper.scraper.spiders.parsers import generic_page_parser, course_parser, reddit_parser
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from sleuth_crawler.scraper.scraper.settings import PARENT_URLS

class BroadCrawler(CrawlSpider):
    """
    Spider that broad crawls starting at list of predefined URLs
    """
    name = "broad_crawler"

    # Root URLs of special page types are stored here
    ROOTS = {
        'courses':'courses.students.ubc.ca',
        'reddit':'www.reddit.com'
    }

    # These are the links that the crawler starts crawling at
    start_urls = PARENT_URLS

    # Rules for what links are followed are defined here
    GENERIC_LINK_EXTRACTOR = LinkExtractor(
        allow=(r'ubc', r'university', r'ubyssey', r'prof', r'student'),
        deny=(r'accounts\.google', r'intent', r'lang=')
    )
    rules = (
        Rule(
            GENERIC_LINK_EXTRACTOR,
            follow=True,
            process_request='process_req',
            callback='parse_generic_item'
        ),
    )

    # Specifies the pipeline that handles data returned from the parsers
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.SolrPipeline': 400,
        }
    }

    def process_req(self, req):
        '''
        Work on requests to identify those that qualify for special treatment
        '''
        # Parse courseItem
        if self.ROOTS['courses'] in req.url:
            # This is the root Course page that starts the course parser
            if 'cs/main?pname=subjarea&tname=subjareas&req=0' in req.url:
                return req.replace(
                    callback=course_parser.parse_subjects,
                    priority=100
                )
            else:
                return

        # Parse redditPost
        if self.ROOTS['reddit'] in req.url:
            if 'comments' in req.url:
                return req.replace(
                    callback=self.parse_reddit_post,
                    priority=100
                )
            else:
                return req.replace(
                    callback=self.no_parse,
                    priority=80
                )

        return req

    def parse_generic_item(self, response):
        '''
        Points to generic_page_parser (the default parser for this crawler)
        '''
        links = self._get_links(response)
        return generic_page_parser.parse_generic_item(response, links)

    def parse_reddit_post(self, response):
        '''
        Points to reddit_parser.parse_comments
        '''
        links = self._get_links(response)
        return reddit_parser.parse_post(response, links)

    def no_parse(self, response):
        '''
        Visit page without parsing it - this allows the URLS of this page to
        be extracted and visited if there are any relevant links
        '''
        return

    def _get_links(self, response):
        links = []
        for link in self.GENERIC_LINK_EXTRACTOR.extract_links(response):
            if link.url != response.url:
                links.append(link.url)
        return links
