import scrapy
from scrapy.spiders import Spider

class CustomCrawler(Spider):
    '''
    Spider that crawls specific domains for specific item types
    that don't link to genericItem
    '''
    name = 'custom_crawler'

    # Specifies the pipeline that handles data returned from the parsers
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.SolrPipeline': 400,
        }
    }

    def __init__(self, start_urls, parser):
        '''
        Takes a list of starting urls and a callback for each link visited
        '''
        self.start_urls = start_urls
        self.parse = parser
