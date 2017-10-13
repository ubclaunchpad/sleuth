import scrapy
import re
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from sleuth_crawler.scraper.scraper.items import GenericPage

class UbcBroadCrawler(CrawlSpider):
    """
    Spider that crawls generically starting at UBC's homepage
    """
    name = "ubc_broad"

    start_urls = ["http://www.ubc.ca"]
    allowed = ['ubc', 'universityofbc']
    rules = (
        Rule(
            LinkExtractor(
                allow=('ubc', 'universityofbc', ), 
                deny=('youtube', 'twitter', 'facebook')
            ),
            callback='parse_item'
        ),
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.SolrPipeline': 400,
            'scraper.pipelines.JsonLogPipeline': 300,
        }
    }

    def parse_item(self, response):
        """
        Scrape page
        """
        output = GenericPage()
        output['url'] = response.url
        output['page_data'] = re.sub(r'<[^>]*?>', '', str(response.body))
        return output