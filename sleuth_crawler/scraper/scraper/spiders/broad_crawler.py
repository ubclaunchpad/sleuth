import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from sleuth_crawler.scraper.scraper.settings import PARENT_URLS
from sleuth_crawler.scraper.scraper.items import ScrapyGenericPage
from bs4 import BeautifulSoup

class BroadCrawler(CrawlSpider):
    """
    Spider that broad crawls starting at list of predefined URLs
    """
    name = "broad_crawler"

    start_urls = PARENT_URLS
    allowed = ['ubc', 'universityofbc']
    rules = (
        Rule(
            LinkExtractor(
                allow=('ubc', 'universityofbc', ),
                deny=('accounts\.google', 'intent', )
            ),
            follow=True,
            callback='parse_item'
        ),
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.SolrPipeline': 400,
        }
    }

    def parse_item(self, response):
        """
        Scrape page
        """
        title = self.__extract_element(response.xpath("//title/text()"), 0)
        desc = self.__extract_element(response.xpath("//meta[@name='description']/@content"), 0)
        raw_content = self.__strip_content(response.body)

        return ScrapyGenericPage(
            url=response.url,
            title=title,
            description=desc,
            raw_content=raw_content
        )

    def __strip_content(self, data):
        try:
            # strip JavaScript, HTML
            soup = BeautifulSoup(data, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            data = soup.get_text()
            # strip extraneous line breaks and sort into list
            lines = []
            for line in data.splitlines():
                line = line.strip()
                if line:
                    lines.append(line.strip())
            return lines
        except Exception:
            return None

    def __extract_element(self, list, index):
        try:
            return list[index].extract()
        except IndexError:
            return None
