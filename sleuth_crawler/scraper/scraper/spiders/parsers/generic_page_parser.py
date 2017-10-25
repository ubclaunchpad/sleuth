import scrapy
from sleuth_crawler.scraper.scraper.spiders.parsers import utils
from sleuth_crawler.scraper.scraper.items import ScrapyGenericPage

def parse_generic_item(response, children):
    """
    Scrape generic page
    """
    site_title = ""
    title = utils.extract_element(response.xpath("//title/text()"), 0)
    titles = title.split('|')
    if len(titles) == 2:
        title = titles[0].strip()
        site_title = titles[1].strip()
    desc = utils.extract_element(response.xpath("//meta[@name='description']/@content"), 0)
    raw_content = utils.strip_content(response.body)

    return ScrapyGenericPage(
        url=response.url,
        title=title,
        site_title=site_title,
        description=desc,
        raw_content=raw_content,
        children=children
    )