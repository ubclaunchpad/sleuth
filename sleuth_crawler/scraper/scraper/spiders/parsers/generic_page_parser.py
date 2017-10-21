import scrapy
import sleuth_crawler.scraper.scraper.spiders.parsers.utils as utils
from sleuth_crawler.scraper.scraper.items import ScrapyGenericPage

def parse_generic_item(response, extractor):
    """
    Scrape generic page
    """
    title = utils.extract_element(response.xpath("//title/text()"), 0)
    desc = utils.extract_element(response.xpath("//meta[@name='description']/@content"), 0)
    raw_content = utils.strip_content(response.body)
    children = []
    for link in extractor.extract_links(response):
        children.append(link.url)

    return ScrapyGenericPage(
        url=response.url,
        title=title,
        description=desc,
        raw_content=raw_content,
        children=children
    )