import sys
import os.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path = sys.path + [os.path.join(PROJECT_ROOT, '../../..'), os.path.join(PROJECT_ROOT, '../..')]

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from sleuth_crawler.scraper.scraper.settings import CUSTOM_URLS
from sleuth_crawler.scraper.scraper.spiders.parsers.course_parser import parse_subjects

'''
This script runs all our spiders.
Crawl specific item types, such as CourseItem, before starting the broad_crawler
'''

def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl('broad_crawler')
    process.crawl('custom_crawler', start_urls=CUSTOM_URLS['courseItem'], parser=parse_subjects)
    process.start()

if __name__ == "__main__":
    run()
