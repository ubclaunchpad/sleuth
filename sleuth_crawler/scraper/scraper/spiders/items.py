import scrapy

class GenericPage(scrapy.Item):
    """
    Stores generic page data and url
    """
    url = scrapy.Field()
    page_data = scrapy.Field()
