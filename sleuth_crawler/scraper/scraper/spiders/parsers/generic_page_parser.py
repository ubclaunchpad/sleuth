import scrapy
import re
from sleuth_crawler.scraper.scraper.spiders.parsers import utils
from sleuth_crawler.scraper.scraper.items import ScrapyGenericPage

def parse_generic_item(response, links):
    '''
    Scrape generic page
    '''
    title = utils.extract_element(response.xpath("//title/text()"), 0).strip()
    titles = re.split(r'\| | - ', title)

    # Use OpenGraph title data if available
    if len(response.xpath('//meta[@property="og:site_name"]')) > 0 and \
        len(response.xpath('//meta[@property="og:title"]')) > 0:
        title = utils.extract_element(
            response.xpath('//meta[@property="og:title"]/@content'), 0
        )
        site_title = utils.extract_element(
            response.xpath('//meta[@property="og:site_name"]/@content'), 0
        )
    elif len(titles) >= 2:
        title = titles[0].strip()
        site_titles = []
        for i in range(max(1, len(titles)-2), len(titles)):
            site_titles.append(titles[i].strip())
        site_title = ' - '.join(site_titles)
    else:
        site_title = ''

    # Use OpenGraph description if available
    if len(response.xpath('//meta[@property="og:description"]')) > 0:
        desc = utils.extract_element(
            response.xpath('//meta[@property="og:description"]/@content'), 0
        )
    else:
        desc = utils.extract_element(
            response.xpath('//meta[@name="description"]/@content'), 0
        )

    raw_content = utils.strip_content(response.body)

    return ScrapyGenericPage(
        url=response.url,
        title=title,
        site_title=site_title,
        description=desc,
        raw_content=raw_content,
        links=links
    )
    